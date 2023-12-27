from django.db import models

class CarouselImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='carousel_images/')
    # alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Carousel Image {self.id}"
