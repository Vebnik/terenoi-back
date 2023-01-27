window.addEventListener('load', () => {

  setTimeout(() => {

    function get_unput(id=1) {
      return `
      <p>
        <label for="id_phone_extend">Дополнительный номер телефона</label>
        <input type="text" name="phone" maxlength="25" class="form-control" required="" id="id_phone_extend">
      </p>
      <p>
        <label for="comments">Коментарии</label>
        <input type="text" name="comments" maxlength="25" class="form-control" required="" id="comments">
      </p>
      <p>
        <input class="form-control hidden">
      </p>`
    }

    document.querySelector('#addPhoneBtn').addEventListener('click', (ev) => {
      form = document.querySelector('#userCreateFormBody')
      form.insertAdjacentHTML('beforeend', get_unput())
    })

  })

})