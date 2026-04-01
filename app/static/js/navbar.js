// Navbar toggle functionality
const toggle = document.getElementById('navbarToggle');
const navbar = document.querySelector('.navbar');
const menu = document.querySelector('.navbar__nav');
const actions = document.querySelector('.navbar__actions');
const body = document.body;

// Prevent scroll/touch events when menu is open
function preventScroll(e) {
    e.preventDefault();
    e.stopPropagation();
    return false;
}

if (toggle && navbar) {
	toggle.addEventListener('click', () => {
		const isOpen = navbar.classList.contains('navbar--open');

		navbar.classList.toggle('navbar--open');
		body.classList.toggle('navbar--menu-open', !isOpen);

		// Prevent scroll when menu is open
		if (!isOpen) {
			// Menu is now open - prevent scroll
			document.addEventListener('wheel', preventScroll, { passive: false });
			document.addEventListener('touchmove', preventScroll, { passive: false });
			document.addEventListener('keydown', (e) => {
				// Prevent arrow keys and spacebar
				if ([32, 37, 38, 39, 40].includes(e.keyCode)) {
					preventScroll(e);
				}
			});
		} else {
			// Menu is now closed - allow scroll
			document.removeEventListener('wheel', preventScroll);
			document.removeEventListener('touchmove', preventScroll);
			document.removeEventListener('keydown', (e) => {
				if ([32, 37, 38, 39, 40].includes(e.keyCode)) {
					preventScroll(e);
				}
			});
		}

		const expanded = toggle.getAttribute('aria-expanded') === 'true';
		toggle.setAttribute('aria-expanded', String(!expanded));
		if (menu) {
			menu.setAttribute('aria-hidden', String(expanded));
		}
		if (actions) {
			actions.setAttribute('aria-hidden', String(expanded));
		}
	});
}
