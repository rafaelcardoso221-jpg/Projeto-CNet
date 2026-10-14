"""Testes sem emulador, rede, dependências gráficas ou desktop ativo."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
import random
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

import basebot as b

ROOT = Path(__file__).resolve().parents[1]


def settings():
    return b.Settings.load(ROOT / "config.ini")


def clock(s):
    return b.VirtualClock(threading.Event(), s, random.Random(42))


class ParserTests(unittest.TestCase):
    def test_valid_readings(self):
        for text, expected in (
            ("X: 510 Y: 732\n", (510, 732)),
            ("X:510Y:732", (510, 732)),
            ("510   732", (510, 732)),
            ("x: -10 y: +20", (-10, 20)),
            ("0\n0", (0, 0)),
        ):
            with self.subTest(text=text):
                self.assertEqual(b.parse_xy(text, -1000, 1000), expected)

    def test_rejects_ambiguous_or_partial(self):
        for text in (
            "510732",
            "X:510",
            "Y:732 X:510",
            "5 10 732",
            "X:510 Y:7?2",
            "5.10 732",
            "",
            "8 9 garbage",
        ):
            with self.subTest(text=text), self.assertRaises(b.OCRFailure):
                b.parse_xy(text, -1000, 1000)

    def test_limits(self):
        with self.assertRaises(b.OCRFailure):
            b.parse_xy("X: 9999 Y: 1", 0, 999)

    def test_ranges(self):
        self.assertEqual(b.parse_span("0.5, 0.9", "teste"), b.Span(0.5, 0.9))
        for text in ("1", "1,2,3", "2,1", "-1,2", "nan,3", "0,inf"):
            with self.subTest(text=text), self.assertRaises(b.BotError):
                b.parse_span(text, "teste")


class ConfigurationTests(unittest.TestCase):
    def test_sample_valid(self):
        self.assertEqual(settings().ocr_attempts, 3)

    def test_invalid_time(self):
        for hhmm in ("25:00", "8:00", "12:60", "hello"):
            with self.subTest(hhmm=hhmm), self.assertRaises(b.BotError):
                replace(settings(), start=hhmm).validate()

    def test_nonfinite(self):
        with self.assertRaises(b.BotError):
            replace(settings(), stay_minutes=float("nan")).validate()

    def test_watchdog_upper_bound(self):
        s = settings()
        s.spans["watchdog"] = b.Span(0.1, 0.2)
        with self.assertRaises(b.BotError):
            s.validate()

    def test_webhook_secret_not_in_error(self):
        secret = "https://example.org/secret-token"
        with self.assertRaises(b.BotError) as ctx:
            replace(settings(), webhook=secret).validate()
        self.assertNotIn(secret, str(ctx.exception))

    def test_no_emergency_key_as_keepalive(self):
        with self.assertRaises(b.BotError):
            replace(settings(), keep_key="f12").validate()

    def test_whitelist_rejects_arguments_and_whitespace(self):
        for value in ("0123456789 --psm 0", '0123456789"', "0123456789 -"):
            with self.subTest(value=value), self.assertRaises(b.BotError):
                replace(settings(), whitelist=value).validate()

    def test_missing_config(self):
        with tempfile.TemporaryDirectory() as temp, self.assertRaises(b.BotError):
            b.Settings.load(Path(temp) / "missing.ini")

    def test_missing_setting(self):
        c = b.read_ini(ROOT / "config.ini")
        c.remove_option("tempos", "watchdog")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.ini"
            with path.open("w", encoding="utf-8") as out:
                c.write(out)
            with self.assertRaises(b.BotError):
                b.Settings.load(path)

    def test_sample_calibration_cannot_drive_mouse(self):
        with self.assertRaises(b.BotError):
            b.Calibration.load(ROOT / "calibracao.ini", settings().title)

    def test_calibration_roundtrip_and_title(self):
        cal = b.Calibration(
            1280, 720, (20, 20, 250, 40), (180, 550), 65, settings().title
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "calibracao.ini"
            cal.save(path)
            self.assertEqual(b.Calibration.load(path, cal.title), cal)
            with self.assertRaises(b.BotError):
                b.Calibration.load(path, "Outro emulador")
            self.assertFalse(path.with_suffix(".tmp").exists())

    def test_calibration_geometry(self):
        valid = b.Calibration(1280, 720, (20, 20, 250, 40), (180, 550), 65, "test")
        for bad in (
            replace(valid, radius=0),
            replace(valid, roi=(1200, 20, 250, 40)),
            replace(valid, center=(5, 5)),
        ):
            with self.subTest(cal=bad), self.assertRaises(b.BotError):
                bad.validate()

    def test_every_ini_key_and_section_has_comment(self):
        for path in (ROOT / "config.ini", ROOT / "calibracao.ini"):
            previous = ""
            for line in path.read_text(encoding="utf-8").splitlines():
                if line and not line.startswith(";"):
                    self.assertTrue(previous.startswith(";"), f"{path.name}: {line}")
                previous = line


class SchedulingTests(unittest.TestCase):
    def test_today(self):
        self.assertEqual(
            b.next_start(datetime(2026, 10, 14, 9), "10:30"),
            datetime(2026, 10, 14, 10, 30),
        )

    def test_tomorrow_rollover(self):
        self.assertEqual(
            b.next_start(datetime(2026, 12, 31, 23, 59), "08:00"),
            datetime(2027, 1, 1, 8),
        )

    def test_current_minute_immediate(self):
        now = datetime(2026, 10, 14, 10, 30, 45)
        self.assertEqual(b.next_start(now, "10:30"), now)


class ControlTests(unittest.TestCase):
    def test_tolerance_per_axis(self):
        s = settings()
        self.assertIsNone(
            b.decide(s.x + s.tolerance, s.y - s.tolerance, s, random.Random(1))
        )

    def test_invert_y(self):
        s = settings()
        normal = b.decide(s.x, s.y - 30, s, random.Random(1))
        inverted = b.decide(s.x, s.y - 30, replace(s, invert_y=True), random.Random(1))
        self.assertGreater(normal.uy, 0)
        self.assertLess(inverted.uy, 0)
        self.assertAlmostEqual(normal.ux, 0)

    def test_near_pulse_shorter(self):
        s = settings()
        near = b.decide(s.x - 15, s.y, s, random.Random(1))
        far = b.decide(s.x - 100, s.y, s, random.Random(1))
        self.assertLess(near.seconds, far.seconds)

    def test_simulated_arrival_and_drift_correction(self):
        for invert in (False, True):
            with self.subTest(invert=invert):
                s = replace(
                    settings(), stay_minutes=2, invert_y=invert, keep_alive=True
                )
                c = clock(s)
                desktop = b.SimulatedDesktop(s, c)
                self.assertTrue(b.navigate(desktop, s, c))
                before = desktop.pulses
                start = c.now()
                b.remain(desktop, s, c)
                self.assertGreater(desktop.pulses, before)
                self.assertAlmostEqual(c.now() - start, 120)
                self.assertIsNone(b.decide(*desktop.read_once(), s, c.rng))

    def test_ocr_retry_success(self):
        s, desktop = settings(), Mock()
        c = clock(s)
        desktop.read_once.side_effect = [
            b.OCRFailure("a"),
            b.OCRFailure("b"),
            (s.x, s.y),
        ]
        self.assertEqual(b.read_position(desktop, s, c), (s.x, s.y))
        self.assertEqual(desktop.read_once.call_count, 3)
        self.assertGreater(c.now(), 0)

    def test_ocr_failure_never_moves(self):
        s, desktop = settings(), Mock()
        desktop.read_once.side_effect = b.OCRFailure("no text")
        with self.assertRaises(b.OCRFailure):
            b.navigate(desktop, s, clock(s))
        self.assertEqual(desktop.read_once.call_count, 3)
        desktop.pulse.assert_not_called()

    def test_stagnation_stops(self):
        s, desktop = settings(), Mock()
        s.stagnant_limit = 3
        desktop.read_once.return_value = (s.x - 80, s.y)
        with self.assertRaisesRegex(b.BotError, "Sem progresso"):
            b.navigate(desktop, s, clock(s))
        self.assertEqual(desktop.pulse.call_count, 3)

    def test_navigation_timeout(self):
        s = replace(settings(), navigation_timeout=1)
        c = clock(s)
        desktop = b.SimulatedDesktop(s, c)
        with self.assertRaisesRegex(b.BotError, "Timeout"):
            b.navigate(desktop, s, c)
        self.assertLessEqual(c.now(), 1)

    def test_no_pulse_after_slow_ocr_exceeds_deadline(self):
        s = replace(settings(), navigation_timeout=1)
        c, desktop = clock(s), Mock()

        def slow():
            c.wait(2)
            return s.x - 100, s.y

        desktop.read_once.side_effect = slow
        with self.assertRaisesRegex(b.BotError, "Timeout"):
            b.navigate(desktop, s, c)
        desktop.pulse.assert_not_called()

    def test_window_reconnect_then_arrival(self):
        s, desktop = settings(), Mock()
        desktop.read_once.side_effect = [b.WindowLost("lost"), (s.x, s.y)]
        self.assertTrue(b.navigate(desktop, s, clock(s)))
        desktop.reconnect.assert_called_once_with(None)
        desktop.pulse.assert_not_called()

    def test_failed_reconnect_aborts(self):
        s, desktop = settings(), Mock()
        desktop.read_once.side_effect = b.WindowLost("lost")
        desktop.reconnect.side_effect = b.WindowLost("timeout")
        with self.assertRaises(b.WindowLost):
            b.navigate(desktop, s, clock(s))
        desktop.pulse.assert_not_called()

    def test_expired_stay_never_inputs(self):
        s, desktop = settings(), Mock()
        self.assertFalse(b.navigate(desktop, s, clock(s), stay_deadline=0))
        desktop.pulse.assert_not_called()
        desktop.read_once.assert_not_called()

    def test_sleep_is_interruptible(self):
        stop = threading.Event()
        stop.set()
        c = b.Clock(stop, settings(), random.Random())
        with self.assertRaises(b.Stopped):
            c.wait(600)

    def test_zero_stay_no_keepalive(self):
        s = replace(settings(), stay_minutes=0, keep_alive=True)
        desktop = Mock()
        b.remain(desktop, s, clock(s))
        desktop.keepalive.assert_not_called()
        desktop.read_once.assert_not_called()


class DesktopSafetyTests(unittest.TestCase):
    def test_release_mouse_when_drag_raises(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.cal = b.Calibration(
            1280, 720, (20, 20, 250, 40), (180, 550), 65, "test"
        )
        desktop.begin_input = Mock(return_value=b.Frame(1, 0, 0, 1280, 720))
        desktop.ensure = Mock()
        desktop.pg = Mock()
        desktop.pg.moveTo.side_effect = [None, RuntimeError("drag failed")]
        desktop.native_release = Mock()
        with self.assertRaises(RuntimeError):
            desktop.pulse(b.Motion(1, 0, 0.5))
        desktop.pg.mouseDown.assert_called_once()
        desktop.native_release.assert_called_once()
        self.assertIsNone(desktop.guard)

    def test_release_key_when_wait_raises(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.s, desktop.pg = settings(), Mock()
        desktop.begin_input, desktop.native_release = Mock(), Mock()
        desktop.clock = Mock()
        desktop.clock.delay.side_effect = b.Stopped("stop")
        with self.assertRaises(b.Stopped):
            desktop.keepalive()
        desktop.native_release.assert_called_once()

    def test_focus_guard_rejects_input(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.ensure = Mock(return_value=b.Frame(1, 0, 0, 1280, 720))
        desktop.is_current = Mock(return_value=False)
        with self.assertRaises(b.WindowLost):
            desktop.begin_input()
        self.assertIsNone(desktop.guard)

    def test_emergency_request_does_not_wait_for_ocr(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.emergency = threading.Event()
        desktop.request_emergency("F12")
        self.assertTrue(desktop.emergency.is_set())
        self.assertEqual(desktop.reason, "F12")

    def test_ensure_rejects_stopped_input(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.clock = clock(settings())
        desktop.clock.stop.set()
        with self.assertRaises(b.Stopped):
            desktop.ensure()

    def test_reconnect_timeout_is_bounded(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.s = replace(settings(), reconnect_timeout=70)
        desktop.clock = clock(desktop.s)
        desktop.native_release = Mock()
        desktop.find_window = Mock(return_value=None)
        with self.assertRaises(b.WindowLost):
            desktop.reconnect()
        self.assertEqual(desktop.clock.now(), 70)
        self.assertEqual(desktop.find_window.call_count, 3)
        desktop.native_release.assert_called_once()

    def test_reconnect_respects_stay_deadline(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.s = settings()
        desktop.clock = clock(desktop.s)
        desktop.native_release = Mock()
        desktop.find_window = Mock(return_value=None)
        with self.assertRaises(b.WindowLost):
            desktop.reconnect(overall_deadline=5)
        self.assertEqual(desktop.clock.now(), 5)
        desktop.find_window.assert_called_once()

    def test_resize_requires_recalibration(self):
        desktop = b.Desktop.__new__(b.Desktop)
        desktop.s = settings()
        desktop.clock = clock(desktop.s)
        desktop.cal = b.Calibration(
            1280, 720, (20, 20, 250, 40), (180, 550), 65, "test"
        )
        desktop.native_release = Mock()
        window = Mock(isMinimized=False)
        desktop.find_window = Mock(return_value=window)
        desktop.frame_for = Mock(return_value=b.Frame(1, 0, 0, 640, 480))
        desktop.gw = Mock(PyGetWindowException=RuntimeError)
        with self.assertRaisesRegex(b.BotError, "Tamanho"):
            desktop.reconnect()

    def test_dry_run_notification_has_no_network(self):
        s = replace(
            settings(), webhook="https://discord.com/api/webhooks/123/fake-token"
        )
        # requests não é instalado/requerido pelo teste; dry-run não deve importá-lo.
        with patch.dict("sys.modules", {"requests": None}):
            b.notify(s, clock(s), dry=True)


if __name__ == "__main__":
    unittest.main()
