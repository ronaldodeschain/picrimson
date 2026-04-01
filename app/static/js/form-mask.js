// Apply phone mask on register form
const phoneInput = document.getElementById('phone');
if (phoneInput && window.IMask) {
	IMask(phoneInput, {
		mask: '(##) #####-####'
	});
}
