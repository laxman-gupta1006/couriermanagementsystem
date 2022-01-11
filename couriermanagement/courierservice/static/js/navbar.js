const menuToggle = document.querySelector(".mobile-menu");
const menuClose = document.querySelector(".menu-close");
const nav = document.querySelector(".nav-container");

window.onresize = reportWindowSize;

function reportWindowSize() {
	let width = window.innerWidth;
	if (width >= 768) {
		onMenuToggle("close");
	}
}

function onMenuToggle(toggle) {
	if (toggle === "open") {
		menuToggle.style.display = "none";
		menuClose.style.display = "block";
		nav.style.right = 0;
	} else {
		menuToggle.style.display = "flex";
		menuClose.style.display = "none";
		nav.style.right = "-440px";
	}
}
