document.addEventListener(
    "DOMContentLoaded",
    () => {

        const images = document.querySelectorAll("img");

        images.forEach(image => {

            image.loading = "lazy";

        });

    }
);