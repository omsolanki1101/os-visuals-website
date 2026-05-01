const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll() {
  revealElements.forEach((element) => {
    const elementTop = element.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if (elementTop < windowHeight - 100) {
      element.classList.add("active");
    }
  });
}

window.addEventListener("load", revealOnScroll);
window.addEventListener("scroll", revealOnScroll);

/* Cursor glow */
const cursorGlow = document.querySelector(".cursor-glow");

document.addEventListener("mousemove", (event) => {
  cursorGlow.style.left = event.clientX + "px";
  cursorGlow.style.top = event.clientY + "px";
  cursorGlow.style.opacity = "1";
});

document.addEventListener("mouseleave", () => {
  cursorGlow.style.opacity = "0";
});