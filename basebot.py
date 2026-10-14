#!/usr/bin/env python3
"""RPA visual para Windows. Python 3.10+; nenhum acesso interno ao aplicativo.

Uso: basebot.py | --calibrar | --dry-run | --validar-config
As dependências gráficas só são importadas na execução real, não na simulação.
"""

from __future__ import annotations

import argparse
import configparser
import ctypes
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import math
import os
from pathlib import Path
import queue
import random
import re
import shutil
import subprocess
import sys
import threading
import time

ROOT = (
    Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent
)
LOG = logging.getLogger("basebot")


class BotError(Exception):
    """Erro explicável ao usuário, sem prosseguir com inputs às cegas."""


class WindowLost(BotError):
    pass


class OCRFailure(BotError):
    pass


class Stopped(BotError):
    pass


@dataclass(frozen=True)
class Span:
    low: float
    high: float

    def sample(self, rng: random.Random) -> float:
        return rng.uniform(self.low, self.high)


def parse_span(value: str, name: str, minimum: float = 0.0) -> Span:
    """Faixas usam ponto decimal e vírgula entre mínimo e máximo."""
    try:
        a, b = (float(x.strip()) for x in value.split(","))
    except (ValueError, TypeError) as exc:
        raise BotError(f"{name}: use minimo,maximo (ex.: 0.5,0.9).") from exc
    if not all(math.isfinite(x) for x in (a, b)) or a < minimum or b < a:
        raise BotError(f"Faixa inválida em {name}: {value}")
    return Span(a, b)


def read_ini(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser(interpolation=None, inline_comment_prefixes=None)
    try:
        with path.open(encoding="utf-8-sig") as stream:
            parser.read_file(stream)
    except (OSError, configparser.Error) as exc:
        raise BotError(f"Não foi possível ler {path.name}: {exc}") from exc
    return parser


def finite(value: float, name: str, minimum: float, maximum: float) -> float:
    if not math.isfinite(value) or not minimum <= value <= maximum:
        raise BotError(f"{name}: valor fora do intervalo {minimum} a {maximum}.")
    return value


@dataclass
class Settings:
    x: int
    y: int
    start: str
    stay_minutes: float
    tolerance: int
    invert_y: bool
    title: str
    emulator: str
    tesseract: str
    threshold: int
    invert_image: bool
    whitelist: str
    ocr_attempts: int
    coord_min: int
    coord_max: int
    slow_distance: float
    angle_jitter: float
    navigation_timeout: float
    stagnant_limit: int
    reconnect_timeout: float
    validation_seconds: float
    keep_alive: bool
    keep_key: str
    webhook: str
    notify_failure_fatal: bool
    spans: dict[str, Span]

    @classmethod
    def load(cls, path: Path) -> Settings:
        c = read_ini(path)
        try:
            spans = {
                name: parse_span(c["tempos"][name], name, 0.001)
                for name in (
                    "pulso",
                    "pulso_perto",
                    "entre_pulsos",
                    "retry_ocr",
                    "timeout_ocr",
                    "verificacao_posicao",
                    "keep_alive",
                    "duracao_tecla",
                    "reconexao",
                    "apos_foco",
                    "contagem",
                    "validacao",
                    "watchdog",
                    "timeout_webhook",
                )
            }
            s = cls(
                c.getint("rotina", "alvo_x"),
                c.getint("rotina", "alvo_y"),
                c["rotina"]["hora_inicio"].strip(),
                c.getfloat("rotina", "minutos_permanencia"),
                c.getint("rotina", "tolerancia"),
                c.getboolean("rotina", "inverter_y"),
                c["janela"]["titulo"].strip(),
                c["janela"]["caminho_emulador"].strip(),
                c["ocr"]["caminho_tesseract"].strip(),
                c.getint("ocr", "threshold"),
                c.getboolean("ocr", "inverter_imagem"),
                c["ocr"]["whitelist"].strip(),
                c.getint("ocr", "tentativas"),
                c.getint("ocr", "coordenada_minima"),
                c.getint("ocr", "coordenada_maxima"),
                c.getfloat("controle", "distancia_desaceleracao"),
                c.getfloat("controle", "jitter_angular_graus"),
                c.getfloat("seguranca", "timeout_navegacao"),
                c.getint("seguranca", "limite_sem_progresso"),
                c.getfloat("seguranca", "timeout_reconexao"),
                c.getfloat("calibracao", "segundos_validacao"),
                c.getboolean("keep_alive", "habilitado"),
                c["keep_alive"]["tecla"].strip().lower(),
                c["notificacoes"]["webhook_discord"].strip(),
                c.getboolean("notificacoes", "falha_fatal"),
                spans,
            )
        except (KeyError, ValueError, configparser.Error) as exc:
            raise BotError(f"config.ini incompleto ou inválido: {exc}") from exc
        s.validate()
        return s

    def validate(self) -> None:
        if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", self.start):
            raise BotError("hora_inicio deve ser HH:MM, de 00:00 a 23:59.")
        finite(self.stay_minutes, "minutos_permanencia", 0, 10080)
        finite(self.tolerance, "tolerancia", 0, 100000)
        finite(self.threshold, "threshold", 0, 255)
        finite(self.slow_distance, "distancia_desaceleracao", 1, 1000000)
        finite(self.angle_jitter, "jitter_angular_graus", 0, 15)
        finite(self.navigation_timeout, "timeout_navegacao", 1, 86400)
        finite(self.reconnect_timeout, "timeout_reconexao", 1, 3600)
        finite(self.validation_seconds, "segundos_validacao", 1, 60)
        if (
            not self.title
            or not 1 <= self.ocr_attempts <= 10
            or self.stagnant_limit < 1
        ):
            raise BotError("Confira título, tentativas de OCR e limite_sem_progresso.")
        if (
            not self.coord_min
            <= min(self.x, self.y)
            <= max(self.x, self.y)
            <= self.coord_max
        ):
            raise BotError("Alvos fora dos limites de coordenadas configurados.")
        if self.spans["watchdog"].high > 0.1:
            raise BotError("watchdog deve ser no máximo 0.1 s para a parada rápida.")
        if not re.fullmatch(r"[0-9XYxy:+\-]+", self.whitelist) or not all(
            d in self.whitelist for d in "0123456789"
        ):
            raise BotError(
                "whitelist deve conter os dez dígitos; só XYxy, sinais e : são opcionais (sem espaços)."
            )
        if self.keep_key not in ("shift", "ctrl", "alt", "space") and not re.fullmatch(
            r"[a-z0-9]", self.keep_key
        ):
            raise BotError(
                "keep_alive.tecla: use uma letra, dígito, shift, ctrl, alt ou space (nunca F12)."
            )
        if self.webhook and not re.fullmatch(
            r"https://(?:canary\.|ptb\.)?discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_.-]+",
            self.webhook,
        ):
            raise BotError(
                "webhook_discord deve ser uma URL HTTPS de webhook do Discord, sem parâmetros."
            )


@dataclass(frozen=True)
class Frame:
    hwnd: int
    left: int
    top: int
    width: int
    height: int


@dataclass(frozen=True)
class Calibration:
    width: int
    height: int
    roi: tuple[int, int, int, int]
    center: tuple[int, int]
    radius: int
    title: str

    def validate(self) -> None:
        x, y, w, h = self.roi
        cx, cy = self.center
        if self.width <= 0 or self.height <= 0 or min(x, y) < 0 or w < 4 or h < 4:
            raise BotError("Região OCR inválida. Execute CALIBRAR.bat.")
        if x + w > self.width or y + h > self.height or self.radius < 2:
            raise BotError("OCR/raio fora da área cliente. Recalibre.")
        if not (
            self.radius <= cx < self.width - self.radius
            and self.radius <= cy < self.height - self.radius
        ):
            raise BotError("Joystick e seu raio devem caber inteiramente na janela.")

    @classmethod
    def load(cls, path: Path, title: str) -> Calibration:
        c = read_ini(path)
        try:
            if not c.getboolean("calibracao", "calibrado"):
                raise BotError("Ainda não há calibração. Execute CALIBRAR.bat uma vez.")
            g = c["calibracao"]
            result = cls(
                g.getint("largura_cliente"),
                g.getint("altura_cliente"),
                tuple(
                    g.getint(k) for k in ("ocr_x", "ocr_y", "ocr_largura", "ocr_altura")
                ),
                (g.getint("joystick_x"), g.getint("joystick_y")),
                g.getint("joystick_raio"),
                g["titulo"],
            )
        except (KeyError, ValueError, configparser.Error) as exc:
            raise BotError(f"calibracao.ini inválido: {exc}") from exc
        result.validate()
        if result.title != title:
            raise BotError(
                "O título configurado mudou. Recalibre para a janela correta."
            )
        return result

    def save(self, path: Path) -> None:
        self.validate()
        x, y, w, h = self.roi
        content = (
            "; Gerado pelo assistente; posições em pixels físicos relativos à área cliente.\n"
            "; Não reutilize após alterar resolução, zoom, DPI ou layout do aplicativo.\n"
            "[calibracao]\n; Somente o assistente deve habilitar esta opção.\ncalibrado = sim\n"
            f"; Título exato da janela calibrada.\ntitulo = {self.title}\n"
            f"; Largura da área cliente.\nlargura_cliente = {self.width}\n"
            f"; Altura da área cliente.\naltura_cliente = {self.height}\n"
            f"; Borda esquerda da leitura.\nocr_x = {x}\n; Borda superior da leitura.\nocr_y = {y}\n"
            f"; Largura da leitura.\nocr_largura = {w}\n; Altura da leitura.\nocr_altura = {h}\n"
            f"; Centro horizontal do joystick.\njoystick_x = {self.center[0]}\n"
            f"; Centro vertical do joystick.\njoystick_y = {self.center[1]}\n"
            f"; Distância do centro ao ponto marcado com F4.\njoystick_raio = {self.radius}\n"
        )
        tmp = path.with_suffix(".tmp")
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)  # Não deixa um arquivo parcialmente escrito.


# ConfigParser não reconhece sim/não nativamente.
configparser.ConfigParser.BOOLEAN_STATES = {
    **configparser.ConfigParser.BOOLEAN_STATES,
    "sim": True,
    "nao": False,
    "não": False,
}


def parse_xy(text: str, minimum: int, maximum: int) -> tuple[int, int]:
    """Aceita X: 510 Y: 732 ou exatamente dois números, em ordem X/Y.

    Uma whitelist estritamente numérica pode remover separadores. Nunca se
    adivinha onde dividir um único número: tal leitura causa retry seguro.
    """
    clean = text.strip()
    labelled = re.fullmatch(r"[Xx]\s*:?\s*([+-]?\d+)\s*[Yy]\s*:?\s*([+-]?\d+)", clean)
    numeric = re.fullmatch(r"([+-]?\d+)\s+([+-]?\d+)", clean)
    match = labelled or numeric
    if not match:
        raise OCRFailure(f"Leitura ambígua/incompleta: {clean!r}")
    x, y = map(int, match.groups())
    if not minimum <= x <= maximum or not minimum <= y <= maximum:
        raise OCRFailure(f"Coordenadas fora dos limites: X={x} Y={y}")
    return x, y


def next_start(now: datetime, hhmm: str) -> datetime:
    hour, minute = map(int, hhmm.split(":"))
    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    # Abrir durante o minuto agendado inicia imediatamente, não amanhã.
    if now.hour == hour and now.minute == minute:
        return now
    return candidate if candidate > now else candidate + timedelta(days=1)


@dataclass(frozen=True)
class Motion:
    ux: float
    uy: float
    seconds: float


def decide(x: int, y: int, s: Settings, rng: random.Random) -> Motion | None:
    dx, dy = s.x - x, s.y - y
    if abs(dx) <= s.tolerance and abs(dy) <= s.tolerance:
        return None
    # Um eixo já dentro da tolerância não precisa ser perturbado.
    dx = 0 if abs(dx) <= s.tolerance else dx
    dy = 0 if abs(dy) <= s.tolerance else dy
    sy = -dy if s.invert_y else dy
    angle = math.atan2(sy, dx) + math.radians(
        rng.uniform(-s.angle_jitter, s.angle_jitter)
    )
    near = max(abs(dx), abs(dy)) <= s.slow_distance
    duration = s.spans["pulso_perto" if near else "pulso"].sample(rng)
    return Motion(math.cos(angle), math.sin(angle), duration)


class Clock:
    def __init__(self, stop: threading.Event, s: Settings, rng: random.Random):
        self.stop, self.s, self.rng = stop, s, rng

    def now(self) -> float:
        return time.monotonic()

    def wait(self, seconds: float) -> None:
        if self.stop.wait(max(0, seconds)):
            raise Stopped("Execução interrompida.")

    def delay(self, name: str, deadline: float | None = None) -> None:
        seconds = self.s.spans[name].sample(self.rng)
        if deadline is not None:
            seconds = min(seconds, max(0, deadline - self.now()))
        self.wait(seconds)


class VirtualClock(Clock):
    """Relógio da simulação: não espera tempo real e não toca no desktop."""

    elapsed = 0.0

    def now(self) -> float:
        return self.elapsed

    def wait(self, seconds: float) -> None:
        if self.stop.is_set():
            raise Stopped("Simulação interrompida.")
        self.elapsed += max(0, seconds)


def setup_dpi() -> None:
    """Evita misturar pixels lógicos e físicos no Windows com escala 125%+."""
    if sys.platform != "win32":
        raise BotError("Execução real requer Windows. Neste sistema use --dry-run.")
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except AttributeError:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)


class Desktop:
    """Adaptador real. Todo movimento é condicionado à janela calibrada."""

    def __init__(self, s: Settings, clock: Clock):
        setup_dpi()
        try:
            import pyautogui
            import pygetwindow
            import pytesseract
            from PIL import Image, ImageOps
            from pynput import keyboard
        except ImportError as exc:
            raise BotError(
                "Dependências ausentes. Veja a instalação no README."
            ) from exc
        self.pg, self.gw, self.ocr = pyautogui, pygetwindow, pytesseract
        self.Image, self.ImageOps, self.keyboard = Image, ImageOps, keyboard
        self.s, self.clock = s, clock
        self.pg.PAUSE = (
            0  # Todas as pausas são explícitas, configuráveis e canceláveis.
        )
        self.pg.FAILSAFE = True
        self.user32 = ctypes.windll.user32
        # HWND tem 64 bits em Windows x64; não deixar o ctypes truncá-lo.
        from ctypes import wintypes

        self.wt = wintypes
        self.user32.GetForegroundWindow.restype = wintypes.HWND
        self.user32.IsWindow.argtypes = [wintypes.HWND]
        self.user32.IsIconic.argtypes = [wintypes.HWND]
        self.user32.GetClientRect.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(wintypes.RECT),
        ]
        self.user32.ClientToScreen.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(wintypes.POINT),
        ]
        self.guard: Frame | None = None
        self.lost = threading.Event()
        self.closing = threading.Event()
        self.emergency = threading.Event()
        self.reason = "Parada de emergência"
        self.marks: queue.Queue = queue.Queue()
        self.listener = None
        self.watch_thread = None
        self.cal: Calibration | None = None
        self.frame: Frame | None = None
        self.find_tesseract()

    def find_tesseract(self) -> None:
        candidates = [self.s.tesseract, shutil.which("tesseract")]
        for env in ("ProgramFiles", "LOCALAPPDATA"):
            candidates.append(
                str(Path(os.environ.get(env, "C:/")) / "Tesseract-OCR/tesseract.exe")
            )
        path = next((p for p in candidates if p and Path(p).is_file()), None)
        if not path:
            raise BotError(
                "Tesseract não encontrado. Instale-o ou ajuste ocr.caminho_tesseract."
            )
        self.ocr.pytesseract.tesseract_cmd = path

    def native_release(self) -> None:
        """Liberação sem PyAutoGUI: funciona inclusive com FAILSAFE disparado."""
        self.user32.mouse_event(0x0004, 0, 0, 0, 0)  # LEFTUP
        # Só a tecla configurada pode ser mantida pelo bot.
        key = {"shift": 0x10, "ctrl": 0x11, "alt": 0x12, "space": 0x20}.get(
            self.s.keep_key
        )
        if key is None:
            key = ord(self.s.keep_key.upper())
        self.user32.keybd_event(key, 0, 0x0002, 0)  # KEYUP

    def request_emergency(self, reason: str) -> None:
        self.reason = reason
        self.emergency.set()

    def on_press(self, key) -> None:
        if key == self.keyboard.Key.f12:
            self.request_emergency("F12 pressionado")
        elif key in (
            self.keyboard.Key.f1,
            self.keyboard.Key.f2,
            self.keyboard.Key.f3,
            self.keyboard.Key.f4,
        ):
            point = self.wt.POINT()
            self.user32.GetCursorPos(ctypes.byref(point))
            self.marks.put((key, point.x, point.y, self.user32.GetForegroundWindow()))

    def frame_for(self, hwnd: int) -> Frame:
        if not self.user32.IsWindow(hwnd) or self.user32.IsIconic(hwnd):
            raise WindowLost("Janela ausente ou minimizada.")
        rect, point = self.wt.RECT(), self.wt.POINT()
        if not self.user32.GetClientRect(
            hwnd, ctypes.byref(rect)
        ) or not self.user32.ClientToScreen(hwnd, ctypes.byref(point)):
            raise WindowLost("Não foi possível obter a área cliente.")
        return Frame(hwnd, point.x, point.y, rect.right, rect.bottom)

    def is_current(self, frame: Frame) -> bool:
        try:
            return (
                self.user32.GetForegroundWindow() == frame.hwnd
                and self.frame_for(frame.hwnd) == frame
            )
        except WindowLost:
            return False

    def watchdog(self) -> None:
        """Thread independente do OCR/rede; emergência libera e encerra o processo.

        A saída abrupta é deliberada. Não depende de OCR, finally, foco ou da
        thread principal. O alvo <1s precisa ser medido no PC real (não RTOS).
        """
        rng = random.Random()
        while not self.closing.is_set():
            point = self.wt.POINT()
            if (
                self.user32.GetCursorPos(ctypes.byref(point))
                and point.x == 0
                and point.y == 0
            ):
                self.request_emergency("Mouse no canto (0,0)")
            if (
                self.listener is not None
                and not self.listener.is_alive()
                and not self.closing.is_set()
            ):
                self.request_emergency("Listener F12 indisponível; parada preventiva")
            if self.emergency.is_set():
                self.clock.stop.set()
                self.native_release()
                # Logging em outra thread não pode atrasar a liberação ou a saída.
                writer = threading.Thread(
                    target=LOG.critical,
                    args=("EMERGÊNCIA: %s", self.reason),
                    daemon=True,
                )
                writer.start()
                writer.join(timeout=0.1)
                self.native_release()  # Repete imediatamente antes de matar todas as threads.
                os._exit(130)
            guarded = self.guard
            if guarded is not None and not self.is_current(guarded):
                self.lost.set()
                self.native_release()
            self.closing.wait(self.s.spans["watchdog"].sample(rng))

    def start_safety(self) -> None:
        self.listener = self.keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.watch_thread = threading.Thread(
            target=self.watchdog, name="seguranca", daemon=True
        )
        self.watch_thread.start()

    def close(self) -> None:
        self.guard = None
        self.native_release()
        self.closing.set()
        if self.listener:
            self.listener.stop()
        if self.watch_thread:
            self.watch_thread.join(timeout=self.s.spans["watchdog"].high * 2)

    def open_emulator(self) -> None:
        if not self.s.emulator:
            return
        if self.find_window() is not None:
            return
        path = Path(os.path.expandvars(self.s.emulator)).expanduser()
        if not path.is_file():
            raise BotError("caminho_emulador não é um arquivo executável existente.")
        subprocess.Popen([str(path)], cwd=str(path.parent), shell=False)
        LOG.info("Abertura do emulador solicitada; app/login devem estar preparados.")

    def find_window(self):
        matches = [w for w in self.gw.getAllWindows() if w.title == self.s.title]
        if len(matches) > 1:
            raise BotError(
                "Mais de uma janela com o mesmo título; feche as instâncias extras."
            )
        return matches[0] if matches else None

    def reconnect(self, overall_deadline: float | None = None) -> Frame:
        self.guard = None
        self.native_release()
        deadline = self.clock.now() + self.s.reconnect_timeout
        if overall_deadline is not None:
            deadline = min(deadline, overall_deadline)
        while self.clock.now() < deadline:
            window = self.find_window()
            if window is not None:
                try:
                    if window.isMinimized:
                        window.restore()
                    window.activate()
                    self.clock.delay("apos_foco", deadline)
                    frame = self.frame_for(window._hWnd)
                    if self.cal and (frame.width, frame.height) != (
                        self.cal.width,
                        self.cal.height,
                    ):
                        raise BotError(
                            "Tamanho da janela mudou: restaure o tamanho calibrado ou recalibre."
                        )
                    if (
                        frame.left < 0
                        or frame.top < 0
                        or frame.left + frame.width > self.pg.size().width
                        or frame.top + frame.height > self.pg.size().height
                    ):
                        raise BotError(
                            "Mantenha toda a janela no monitor principal (sem bordas cortadas)."
                        )
                    if self.is_current(frame):
                        self.frame = frame
                        self.lost.clear()
                        LOG.info(
                            "Janela conectada: área=%dx%d origem=(%d,%d)",
                            frame.width,
                            frame.height,
                            frame.left,
                            frame.top,
                        )
                        return frame
                except (WindowLost, self.gw.PyGetWindowException) as exc:
                    LOG.warning("Janela ainda indisponível: %s", exc)
            LOG.warning("Aguardando janela/foco; nova tentativa na faixa reconexao.")
            self.clock.delay("reconexao", deadline)
        raise WindowLost(
            "Prazo para recuperar a janela esgotado; nenhum input será enviado."
        )

    def ensure(self) -> Frame:
        if self.clock.stop.is_set():
            raise Stopped("Input recusado após solicitação de parada.")
        if self.frame is None or self.lost.is_set() or not self.is_current(self.frame):
            raise WindowLost("Janela perdeu foco, mudou de posição ou foi fechada.")
        return self.frame

    def read_once(self) -> tuple[int, int]:
        frame = self.ensure()
        assert self.cal is not None
        x, y, w, h = self.cal.roi
        image = self.pg.screenshot(region=(frame.left + x, frame.top + y, w, h))
        self.ensure()
        image = self.ImageOps.grayscale(image)
        if self.s.invert_image:
            image = self.ImageOps.invert(image)
        image = image.point(lambda p: 255 if p >= self.s.threshold else 0)
        image = image.resize((w * 2, h * 2), self.Image.Resampling.NEAREST)
        try:
            # Sem espaços/aspas: shlex do pytesseract no Windows não as remove.
            # Preservar X/Y é mais seguro que tentar dividir dígitos concatenados.
            config = f"--psm 7 -c preserve_interword_spaces=1 -c tessedit_char_whitelist={self.s.whitelist}"
            raw = self.ocr.image_to_string(
                image,
                lang="eng",
                config=config,
                timeout=self.s.spans["timeout_ocr"].sample(self.clock.rng),
            )
        except (RuntimeError, self.ocr.TesseractError) as exc:
            raise OCRFailure(f"Tesseract falhou: {exc}") from exc
        self.ensure()  # Não usar resultado capturado antes de uma troca de janela.
        LOG.info("OCR bruto=%r", raw.strip())
        return parse_xy(raw, self.s.coord_min, self.s.coord_max)

    def begin_input(self) -> Frame:
        frame = self.ensure()
        self.guard = frame
        if not self.is_current(frame) or self.lost.is_set():
            self.guard = None
            raise WindowLost("Foco perdido antes do input.")
        return frame

    def end_input(self) -> None:
        self.native_release()
        self.guard = None

    def pulse(self, motion: Motion) -> None:
        assert self.cal is not None
        frame = self.begin_input()
        cx, cy = self.cal.center
        cx, cy = frame.left + cx, frame.top + cy
        ex = round(cx + self.cal.radius * motion.ux)
        ey = round(cy + self.cal.radius * motion.uy)
        try:
            self.pg.moveTo(cx, cy)
            self.ensure()
            self.pg.mouseDown(button="left")
            self.ensure()
            self.pg.moveTo(ex, ey)
            self.clock.wait(motion.seconds)
            self.ensure()
        finally:
            self.end_input()

    def keepalive(self) -> None:
        self.begin_input()
        try:
            self.pg.keyDown(self.s.keep_key)
            self.clock.delay("duracao_tecla")
            self.ensure()
        finally:
            self.end_input()
        LOG.info(
            "Keep-alive: tecla %s (não garante que o app considere atividade).",
            self.s.keep_key,
        )


class SimulatedDesktop:
    """Mundo simples com deslocamento e uma deriva programada, sem dependências."""

    def __init__(self, s: Settings, clock: Clock):
        self.s, self.clock = s, clock
        self.x, self.y = float(s.x - 80), float(s.y - 60)
        self.drift_pending = False
        self.pulses = 0

    def reconnect(self, overall_deadline=None):
        LOG.info("SIMULAÇÃO: janela conectada.")

    def read_once(self):
        if self.drift_pending:
            self.x += max(25, self.s.tolerance * 3)
            self.y -= max(20, self.s.tolerance * 3)
            self.drift_pending = False
            LOG.info("SIMULAÇÃO: deriva aplicada.")
        return parse_xy(
            f"{round(self.x)} {round(self.y)}", self.s.coord_min, self.s.coord_max
        )

    def pulse(self, motion: Motion):
        self.pulses += 1
        self.x += motion.ux * motion.seconds * 35
        self.y += motion.uy * motion.seconds * 35 * (-1 if self.s.invert_y else 1)
        self.clock.wait(motion.seconds)

    def keepalive(self):
        LOG.info("SIMULAÇÃO: keep-alive, sem enviar tecla.")
        self.clock.delay("duracao_tecla")


def read_position(
    desktop, s: Settings, clock: Clock, deadline: float | None = None
) -> tuple[int, int]:
    for attempt in range(1, s.ocr_attempts + 1):
        if deadline is not None and clock.now() >= deadline:
            raise BotError("Prazo esgotado antes da próxima leitura OCR.")
        try:
            position = desktop.read_once()
            LOG.info("Leitura X=%d Y=%d (tentativa %d)", *position, attempt)
            return position
        except OCRFailure as exc:
            LOG.warning("OCR tentativa %d/%d: %s", attempt, s.ocr_attempts, exc)
            if attempt < s.ocr_attempts:
                clock.delay("retry_ocr", deadline)
    raise OCRFailure(
        "OCR falhou em todas as tentativas. Rotina encerrada sem movimento às cegas."
    )


def navigate(
    desktop, s: Settings, clock: Clock, stay_deadline: float | None = None
) -> bool:
    """True = chegou; False = permanência terminou durante uma correção."""
    deadline = clock.now() + s.navigation_timeout
    best = float("inf")
    stagnant = 0
    while True:
        if stay_deadline is not None and clock.now() >= stay_deadline:
            return False
        if clock.now() >= deadline:
            raise BotError(
                "Timeout de navegação: confira OCR, inverter_y, raio e velocidade dos pulsos."
            )
        try:
            x, y = read_position(desktop, s, clock, deadline)
            motion = decide(x, y, s, clock.rng)
            if stay_deadline is not None and clock.now() >= stay_deadline:
                return False
            if clock.now() >= deadline:
                raise BotError(
                    "Timeout de navegação após leitura OCR; nenhum novo pulso enviado."
                )
            if motion is None:
                LOG.info(
                    "Alvo confirmado dentro da tolerância; dx=%d dy=%d",
                    s.x - x,
                    s.y - y,
                )
                return True
            distance = max(abs(s.x - x), abs(s.y - y))
            if distance < best:
                best, stagnant = distance, 0
            else:
                stagnant += 1
            if stagnant >= s.stagnant_limit:
                raise BotError(
                    "Sem progresso/oscilações. Reduza pulso_perto ou corrija a calibração; encerrando."
                )
            cap = min(
                deadline, stay_deadline if stay_deadline is not None else deadline
            )
            motion = Motion(
                motion.ux, motion.uy, min(motion.seconds, max(0, cap - clock.now()))
            )
            LOG.info(
                "Decisão dx=%d dy=%d direção=(%.3f,%.3f) pulso=%.3fs",
                s.x - x,
                s.y - y,
                motion.ux,
                motion.uy,
                motion.seconds,
            )
            desktop.pulse(motion)
            clock.delay("entre_pulsos", cap)
        except WindowLost as exc:
            LOG.warning("Navegação pausada: %s", exc)
            # Reconexão tem orçamento próprio (até 10 min); permanência não se estende.
            before = clock.now()
            if stay_deadline is not None and before >= stay_deadline:
                return False
            desktop.reconnect(stay_deadline)
            deadline += clock.now() - before


def remain(desktop, s: Settings, clock: Clock) -> None:
    deadline = clock.now() + s.stay_minutes * 60
    check_at = clock.now() + s.spans["verificacao_posicao"].sample(clock.rng)
    keep_at = (
        clock.now() + s.spans["keep_alive"].sample(clock.rng)
        if s.keep_alive
        else math.inf
    )
    LOG.info(
        "Permanência iniciada: %.2f min; timer inclui correções e indisponibilidade.",
        s.stay_minutes,
    )
    if isinstance(desktop, SimulatedDesktop):
        desktop.drift_pending = True
    while clock.now() < deadline:
        clock.wait(max(0, min(check_at, keep_at, deadline) - clock.now()))
        if clock.now() >= deadline:
            break
        try:
            if clock.now() >= check_at:
                if not navigate(desktop, s, clock, deadline):
                    break
                check_at = clock.now() + s.spans["verificacao_posicao"].sample(
                    clock.rng
                )
            if s.keep_alive and clock.now() >= keep_at and clock.now() < deadline:
                desktop.keepalive()
                keep_at = clock.now() + s.spans["keep_alive"].sample(clock.rng)
        except WindowLost as exc:
            LOG.warning("Permanência: %s", exc)
            desktop.reconnect(deadline)
            check_at = clock.now()  # Ao recuperar, verificar antes de keep-alive.
    LOG.info("Timer de permanência encerrado.")


def schedule(s: Settings, clock: Clock) -> None:
    target = next_start(datetime.now(), s.start)
    LOG.info(
        "Agendado para %s (horário local do Windows). F12 cancela.",
        target.isoformat(timespec="minutes"),
    )
    print(
        "ATENÇÃO: deixe o app pronto. NÃO interaja com mouse/teclado durante a execução.",
        flush=True,
    )
    while True:
        seconds = (target - datetime.now()).total_seconds()
        if seconds <= 0:
            print("\nIniciando rotina.", flush=True)
            return
        print(
            f"\rInício em {timedelta(seconds=math.ceil(seconds))} — F12 para cancelar.   ",
            end="",
            flush=True,
        )
        clock.wait(min(seconds, s.spans["contagem"].sample(clock.rng)))


def capture_mark(desktop: Desktop, expected, frame: Frame) -> tuple[int, int]:
    while True:
        if not desktop.listener.is_alive():
            raise BotError("Listener do teclado parou. Reinicie a calibração.")
        try:
            key, x, y, hwnd = desktop.marks.get_nowait()
        except queue.Empty:
            desktop.clock.delay("watchdog")
            continue
        if key != expected:
            continue
        if hwnd != frame.hwnd or not desktop.is_current(frame):
            raise BotError(
                "Janela mudou/perdeu foco durante a marcação. Recomece a calibração."
            )
        if (
            not frame.left <= x < frame.left + frame.width
            or not frame.top <= y < frame.top + frame.height
        ):
            print("Ponto fora da área cliente. Tente novamente.", flush=True)
            continue
        return x - frame.left, y - frame.top


def calibrate(desktop: Desktop, path: Path) -> None:
    print(
        "\nCALIBRAÇÃO: não clique; apenas posicione o mouse e pressione a tecla indicada.\n"
        "F1: canto superior esquerdo do readout completo X/Y.\n"
        "F2: canto inferior direito do mesmo readout (inclua os maiores valores).\n"
        "F3: centro do joystick. F4: borda útil do joystick (define raio).\n"
        "F12 ou mouse em (0,0): emergência. A janela do emulador receberá foco.\n",
        flush=True,
    )
    desktop.open_emulator()
    frame = desktop.reconnect()
    points = []
    for name in ("f1", "f2", "f3", "f4"):
        LOG.info("Calibração: aguardando %s", name.upper())
        points.append(capture_mark(desktop, getattr(desktop.keyboard.Key, name), frame))
    a, b, center, edge = points
    if b[0] <= a[0] or b[1] <= a[1]:
        raise BotError("F2 deve estar abaixo e à direita de F1.")
    cal = Calibration(
        frame.width,
        frame.height,
        (a[0], a[1], b[0] - a[0], b[1] - a[1]),
        center,
        round(math.hypot(edge[0] - center[0], edge[1] - center[1])),
        desktop.s.title,
    )
    cal.validate()
    desktop.cal = cal
    # Tk vem com Python para Windows e é incluído pelo PyInstaller.
    import tkinter as tk
    from PIL import ImageTk

    root = tk.Tk()
    root.withdraw()
    root.title("BaseBot — validação OCR (nenhum movimento)")
    root.attributes("-topmost", True)
    # Coloca o painel em um canto que NÃO encobre o readout capturado.
    sw, sh = desktop.pg.size()
    rx, ry, rw, rh = cal.roi
    roi = (frame.left + rx, frame.top + ry, rw, rh)
    panel = None
    for px, py in ((sw - 580, sh - 300), (10, sh - 300), (sw - 580, 10), (10, 10)):
        if px < 0 or py < 0:
            continue
        if (
            px + 570 <= roi[0]
            or roi[0] + roi[2] <= px
            or py + 290 <= roi[1]
            or roi[1] + roi[3] <= py
        ):
            panel = (px, py)
            break
    if panel is None:
        root.destroy()
        raise BotError(
            "Sem espaço para mostrar a validação sem cobrir o OCR; reduza a ROI e recalibre."
        )
    root.geometry(f"560x250+{panel[0]}+{panel[1]}")
    root.deiconify()
    label = tk.Label(root, font=("Segoe UI", 14), wraplength=530)
    label.pack(pady=8)
    preview = tk.Label(root)
    preview.pack()
    root.update()
    # A validação pode ser vista sobre o desktop, mas não sobre a ROI.
    desktop.frame = desktop.reconnect()
    frame = desktop.frame
    closed = False

    def cancel():
        nonlocal closed
        closed = True

    root.protocol("WM_DELETE_WINDOW", cancel)
    until = desktop.clock.now() + desktop.s.validation_seconds
    success = 0
    try:
        while desktop.clock.now() < until and not closed:
            try:
                x, y = read_position(desktop, desktop.s, desktop.clock, until)
                success += 1
                label.config(
                    text=f"X: {x}  Y: {y}\nCompare com o app. Restam {max(0, until - desktop.clock.now()):.1f}s"
                )
            except OCRFailure as exc:
                label.config(text=f"Falha OCR: {exc}")
            rx, ry, rw, rh = cal.roi
            image = desktop.pg.screenshot(
                region=(frame.left + rx, frame.top + ry, rw, rh)
            )
            image.thumbnail((520, 95))
            photo = ImageTk.PhotoImage(image)
            preview.config(image=photo)
            preview.image = photo
            root.update()
            # Atualiza a GUI em pequenos passos, sem sleep fixo e sem roubar foco.
            refresh = min(
                until,
                desktop.clock.now()
                + desktop.s.spans["validacao"].sample(desktop.clock.rng),
            )
            while desktop.clock.now() < refresh and not closed:
                root.update()
                desktop.clock.delay("watchdog", refresh)
        if closed or not success:
            raise BotError(
                "Calibração cancelada ou sem leituras válidas; nada foi salvo."
            )
        # Parse válido não prova leitura correta: confirmação humana só neste assistente.
        from tkinter import messagebox

        if not messagebox.askyesno(
            "Confirmar calibração",
            "As coordenadas exibidas coincidiram com o app?\nSalve somente se X e Y estavam corretos.",
            parent=root,
        ):
            raise BotError(
                "Calibração não confirmada; ajuste ROI/threshold/whitelist e tente novamente."
            )
        cal.save(path)
        LOG.info("Calibração validada e salva em %s", path.name)
    finally:
        root.destroy()


def notify(s: Settings, clock: Clock, dry: bool) -> None:
    message = f"concluído às {datetime.now():%H:%M}"
    LOG.info(message)
    print(f"\a{message}", flush=True)
    if not s.webhook:
        return
    if dry:
        LOG.info("SIMULAÇÃO: webhook não enviado.")
        return
    import requests

    try:
        timeout = s.spans["timeout_webhook"].sample(clock.rng)
        # Sem redirects: nunca encaminhar o token a outro host.
        response = requests.post(
            s.webhook,
            json={"content": message},
            timeout=(timeout, timeout),
            allow_redirects=False,
        )
        if not 200 <= response.status_code < 300:
            raise BotError(f"Discord respondeu HTTP {response.status_code}.")
        LOG.info("Aviso Discord entregue.")
    except (requests.RequestException, BotError) as exc:
        # Exceções requests podem conter URL/token; não registrar str(exc).
        LOG.warning(
            "Falha no aviso Discord (%s); URL/token omitidos.", type(exc).__name__
        )
        if s.notify_failure_fatal:
            raise BotError("Rotina terminou, mas a notificação falhou.") from None


def configure_logging() -> Path:
    directory = ROOT / "logs"
    directory.mkdir(exist_ok=True)
    path = directory / f"exec_{datetime.now():%Y-%m-%d_%H-%M}.log"
    LOG.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    for handler in (
        logging.FileHandler(path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ):
        handler.setFormatter(fmt)
        LOG.addHandler(handler)
    return path


def acquire_instance():
    """Impede dois bots/calibrações simultâneos na mesma sessão Windows."""
    if sys.platform != "win32":
        return None
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    kernel.CreateMutexW.restype = wintypes.HANDLE
    handle = kernel.CreateMutexW(None, False, "Local\\BaseBotVisualRPA")
    error = ctypes.get_last_error()
    if not handle:
        raise BotError("Não foi possível criar trava de execução única.")
    if error == 183:
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle(handle)
        raise BotError(
            "Já há um BaseBot/calibração aberto. Feche-o antes de iniciar outro."
        )
    return handle  # O Windows libera ao encerrar o processo.


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--calibrar", action="store_true")
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula sem mouse/OCR/rede e sem esperar o agendamento",
    )
    group.add_argument(
        "--validar-config", action="store_true", help="Só valida config.ini"
    )
    parser.add_argument("--config", type=Path, default=ROOT / "config.ini")
    args = parser.parse_args(argv)
    desktop = None
    try:
        logfile = configure_logging()
        LOG.info(
            "=== BaseBot iniciado; modo=%s; Python=%s ===",
            "dry-run"
            if args.dry_run
            else "calibração"
            if args.calibrar
            else "validação"
            if args.validar_config
            else "real",
            sys.version.split()[0],
        )
        print(f"Log: {logfile}", flush=True)
        s = Settings.load(args.config)
        if args.validar_config:
            LOG.info("config.ini válido. Isso não valida OCR, calibração ou app.")
            return 0
        stop, rng = threading.Event(), random.Random(42 if args.dry_run else None)
        clock = (VirtualClock if args.dry_run else Clock)(stop, s, rng)
        if args.dry_run:
            LOG.info(
                "SIMULAÇÃO: agendamento ignorado; relógio virtual; nenhum input, OCR ou webhook real."
            )
            desktop = SimulatedDesktop(s, clock)
            desktop.reconnect()
        else:
            acquire_instance()
            desktop = Desktop(s, clock)
            desktop.start_safety()
            if args.calibrar:
                calibrate(desktop, ROOT / "calibracao.ini")
                return 0
            desktop.cal = Calibration.load(ROOT / "calibracao.ini", s.title)
            schedule(s, clock)
            desktop.open_emulator()
            desktop.reconnect()
        navigate(desktop, s, clock)
        remain(desktop, s, clock)
        notify(s, clock, args.dry_run)
        LOG.info(
            "Rotina encerrada com sucesso%s.", " (simulada)" if args.dry_run else ""
        )
        return 0
    except KeyboardInterrupt:
        LOG.warning("Interrompido por Ctrl+C.")
        return 130
    except Stopped as exc:
        LOG.warning("Parada de emergência: %s", exc)
        return 130
    except BotError as exc:
        LOG.error("%s", exc)
        print("Se der erro, envie o arquivo de log. Não envie seu webhook.", flush=True)
        return 1
    except Exception:
        LOG.exception("Erro inesperado; inputs serão liberados.")
        return 1
    finally:
        if isinstance(desktop, Desktop):
            desktop.close()


if __name__ == "__main__":
    raise SystemExit(main())
