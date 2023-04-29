/* Used for the menu background panning effect */
const menu = document.getElementById("menu");
Array.from(document.getElementsByClassName("menuItem"))
    .forEach((item, index) => {
        item.onmouseover = () => {
            menu.style.setProperty("--active-index", index)
        }
    });