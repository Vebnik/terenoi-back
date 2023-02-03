window.addEventListener('load', () => {

  const getNewForm = (form_idx) => {
    return `
    <div style="margin: 5px;">
      <label for="id_additionalusernumber_set-${form_idx}-phone">Дополнительный телефон:</label>   
      <input type="text" name="additionalusernumber_set-${form_idx}-phone" maxlength="25" class="form-control" id="id_additionalusernumber_set-${form_idx}-phone">
    </div>
    <div style="margin: 5px;">
      <label for="id_additionalusernumber_set-${form_idx}-comment">Комментраий:</label>   
      <input type="text" name="additionalusernumber_set-${form_idx}-comment" maxlength="100" class="form-control" id="id_additionalusernumber_set-${form_idx}-comment">
    </div>
    <div></div>`
  }

  $('#addPhoneBtn').click(() => {
    const form_idx = $('#id_additionalusernumber_set-TOTAL_FORMS').val()
    $('#userCreateFormBody').append(getNewForm(form_idx))
    $('#id_additionalusernumber_set-TOTAL_FORMS').val(parseInt(form_idx) + 1)
  })

})