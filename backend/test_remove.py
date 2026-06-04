# test_remove.py

from background_remover import (
    remove_product_background
)

remove_product_background(
    "uploads/products/omega3.jpeg",
    "outputs/product_cutout.png"
)

print("done")