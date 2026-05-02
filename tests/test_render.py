from datetime import time
from i_ink.render import render_train_info_image


def _podkowa_crop(image):
    """Crop to the Podkowa Leśna side of the train panel (right half)."""
    return image.crop((240, 0, 480, 150))


def test_podkowa_position_independent_of_warsaw_count():
    podkowa_trains = [(time(20, 5), "2001"), (time(20, 15), "2002"), (time(20, 25), "2003")]

    img_few_warsaw = render_train_info_image({
        "warsaw":        [(time(20, 10), "1001")],
        "podkowa_lesna": podkowa_trains,
    })

    img_full_warsaw = render_train_info_image({
        "warsaw":        [(time(20, 10), "1001"), (time(20, 20), "1002"), (time(20, 30), "1003")],
        "podkowa_lesna": podkowa_trains,
    })

    assert _podkowa_crop(img_few_warsaw).tobytes() == _podkowa_crop(img_full_warsaw).tobytes()
