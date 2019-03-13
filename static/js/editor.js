(function (window, document) {
    var simplemde = new SimpleMDE({
        toolbar: ["bold", "italic", "heading", "|",
        "code", "quote", "|",
        "unordered-list", "ordered-list", "|",
        "link", "image", "table", "|",
        "preview", "guide"],
        element: document.getElementById('editor',)
    });
}(this, this.document));