(function($) {

	var Listeners = {};
	var Utilities = {};

	/**
	* Ready Event.
	*/
	$(document).ready(function() {

		Utilities.activeMenu();
		
		$(document).on('click', '#new-user-form .clear', Listeners.clearNewUserForm);
		$(document).on('click', '#new-user-form .submit', Listeners.submitNewUserForm);
		$(document).on('click', '#users-list .user-delete', Listeners.userDelete);
		$(document).on('click', '#panding-activation .user-activate', Listeners.userActivate);
		
	});


	Listeners = {


		/**
		* Clear form fields.
		*/
		clearNewUserForm: (event) => {
			event.preventDefault();

			$('input[type=text]').val('');
			$('input[type=password]').val('');
		},


		/**
		* Submit New User Form.
		*/
		submitNewUserForm: (event) => {
			event.preventDefault();

			const headers = {
				'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
			};

			var formData = {};
			$("#new-user-form input").each(function() {
				formData[$(this).attr('data-field')] = $(this).val();
			});
			
			$.ajax({
				url: '/dashboard/user/save',
				type: 'POST',
				headers: headers,
				data: formData,
				success: function(res) {
					$("#new-user-form .submit").notify('User created: "'+ res.username +'".', 'success', { position:"right" });
				},
				error: function(err) {
					$("#new-user-form .submit").notify('Unable to create User.', 'error', { position:"right" });
				}
			});
		},


		/**
		* Delete a User.
		*/
		userDelete: (event) => {
			var username;
			if (event.target.tagName == 'I') {
				username = $(event.target.parentNode.parentNode).attr('data-user');
			} else {
				username = $(event.target.parentNode).attr('data-user');
			}

			if ( confirm(`Are you sure to delete user "${username}" ?`) ) {

				const headers = {
					'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
				};

				$.ajax({
					url: `/dashboard/user/delete/${username}/`,
					type: 'GET',
					headers: headers,
					success: function(res) {
						$.notify('User deleted: "'+ username +'".', 'success', { position:"right" });
						$(`.row-user-${username}`).hide('slow');
						setTimeout(() => {
							$(`.row-user-${username}`).remove();
						}, 1200);
					},
					error: function(err) {
						$.notify(err.exception ? err.exception : 'Unable to delete User.', 'error', { position:"right" });
					}
				});
				return true;
			}
			event.preventDefault();
		},


		/**
		* Activate User.
		*/
		userActivate: (event) => {
			event.preventDefault();

			const headers = {
				'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
			};

			var username;
			if (event.target.tagName == 'I') {
				username = $(event.target.parentNode.parentNode).attr('data-user');
			} else {
				username = $(event.target.parentNode).attr('data-user');
			}
			
			$.ajax({
				url: `/dashboard/user/activate/`,
				type: 'POST',
				headers: headers,
				data: { username: username },
				success: function(res) {
					if (res.status) {
						$.notify('User "'+ username +'" Activated.', 'success', { position:"center" });
						$(`.row-activate-user-${username}`).hide('slow');
						setTimeout(() => {
							$(`.row-activate-user-${username}`).remove();
							location.reload();
						}, 1200);
					} else {
						$.notify('Unable to activate User.', 'error', { position:"center" });
					}
				},
				error: function (err) {
					$.notify('Unable to activate User.', 'error', { position:"center" });
				}
			})
		},
	};


	/**
	* Utilities.
	*/
	Utilities = {

		activeMenu: () => {
			const path = location.href;
			// alert(path)
		},
	};
})(jQuery);