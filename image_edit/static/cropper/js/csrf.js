/* NOTE: This file requires that jQuery be loaded 
   ==============================================
*/

/* Note: Django doesn't set the CSRF token cookie if the view doesn't
render a template containing the csrf_token template tag. To force
Django to set the cookie, use the ensure_csrf_cookie() decorator.
See: https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
*/
function getCsrfToken() {
    /* This is how we get the CSRF token 
        See: https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
    */
    let token = null;
    if (document.cookie && document.cookie != '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            const name = 'csrftoken';
            const nameLength = name.length + 1;
            const cookiePrefix = cookie.substring(0, nameLength);
            if (cookiePrefix === name + '=') {
                token = decodeURIComponent(cookie.substring(nameLength));
                break;
            }
        }
    }
    return token;
}
const csrfToken = getCsrfToken();

/* Provide the CSRF to the AJAX request */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});
