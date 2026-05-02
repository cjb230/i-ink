import atexit
import signal
from unittest.mock import patch, MagicMock
import pytest

import i_ink.main as main


def test_handle_signal_clears_display_once():
    mock_display = MagicMock()
    with patch.object(main, 'DISPLAY', mock_display):
        with pytest.raises(SystemExit):
            main.handle_signal(signal.SIGINT, None)
    mock_display.clear.assert_called_once()


def test_handle_signal_unregisters_atexit():
    with patch('atexit.unregister') as mock_unregister:
        with pytest.raises(SystemExit):
            main.handle_signal(signal.SIGINT, None)
    mock_unregister.assert_called_once_with(main.cleanup)
