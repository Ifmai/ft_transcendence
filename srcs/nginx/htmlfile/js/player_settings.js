const ppTwoFactorAuthToggle = document.getElementById('pp-twoFactorAuth');
ppTwoFactorAuthToggle.addEventListener('change', function() {
	console.log('Two-Factor Authentication:', this.checked ? 'Enabled' : 'Disabled');
});

// Save Changes function
function ppSaveChanges() {
	const firstName = document.getElementById('pp-firstName').value;
	const lastName = document.getElementById('pp-lastName').value;
	const city = document.getElementById('pp-city').value;
	const bio = document.getElementById('pp-bio').value;
	const twoFactorAuth = document.getElementById('pp-twoFactorAuth').checked;

	console.log('Saving changes:', {
		firstName,
		lastName,
		city,
		bio,
		twoFactorAuth
	});

	alert('Changes saved successfully!');
}

// Cancel function
function ppCancel() {
	console.log('Changes cancelled');
	alert('Changes cancelled');
}