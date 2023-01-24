window.addEventListener('load', () => {

  function is_valid_form() {
    for (const el of [...document.querySelectorAll('input'), ...document.querySelectorAll('select')]) {
      if (!el.value) {
        toastr.warning(`Check ${el.name.replace('_', ' ')}`)
        return false
      }
    }
    username = 
    `${document.querySelector('#accountFirstName').value}_${document.querySelector('#accountLastName').value}`
    
    html = `<input required type="text" class="hidden" name="username" value="${username}">`
    document.getElementById('user_create_form').insertAdjacentHTML('beforebegin', html)
    
    return true
  }

  document.querySelector('#submit_btn').addEventListener('click', (ev) => {
    if (!is_valid_form()) {
      ev.preventDefault()
    }
  })
})