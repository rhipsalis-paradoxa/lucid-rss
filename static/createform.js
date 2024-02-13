// Load a preview of the RSS feed given by the user's parser template.
async function loadPreview() {
    const form = document.querySelector('#template');
    const formData = new FormData(form);

    const response = await fetch(window.location.href + "/preview", {
        method: "POST",
        body: formData,
    });

    console.log(await response.text());
}
