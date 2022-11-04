"use strict";
document.addEventListener("DOMContentLoaded", onLoad);
function onLoad() {
    document.forms[0].onsubmit = form_submit;
}
function form_submit() {
    for (var _i = 0, _a = document.forms[0].elements; _i < _a.length; _i++) {
        var input = _a[_i];
        if (input.name) {
            var val = input.value.trim();
            if (val === "")
                input.disabled = true;
        }
    }
}

document.querySelectorAll('.select-box').forEach(function (listItem) {
    listItem.addEventListener('click', function (e) {
        e.stopPropagation();
    })
})

document.addEventListener('click', function (e) {
    if (e.target !== document.querySelectorAll('.select-box')) {
        let currentActive = document.querySelector(".options-container.active");
        if (currentActive) {
            currentActive.classList.remove("active");
        }
    }
})

