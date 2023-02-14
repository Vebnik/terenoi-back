window.addEventListener('load', () => {

  function get_teachers(date, subject, time, weekday) {
    fetch(`/manager/users/api/teacher/?date=${date || ''}&subject=${subject}&time=${time}&weekday=${weekday}`)
        .then(res => res.json())
        .then(data => {

          [...document.querySelector('#id_teacher').children].forEach(el => el.remove());
          [...document.querySelector('#id_group').children].forEach(el => el.remove());

          $('#id_teacher').append($('<option>', { value: '', text: '---------' }))
          $('#id_group').append($('<option>', { value: '', text: '---------' }))

            for(const item of data.data){
                $('#id_teacher').append($('<option>', { value: item.pk, text: item.fullname }))
                $('#id_group').append($('<option>', { value: item.group_pk, text: item.group_name }))
            }
         })
  }
  
  const date = $('#fp-range')
  const time = $('#fp-time')
  const subject = $('#id_subject')
  const weekday = $('#id_weekday')
  
  for (const el of [time, subject, date]) {
    el.change(() => {
      get_teachers(date.val(), subject.val(), time.val(), weekday.val())
    })
  }
    

  function getAllTeacher() {
    fetch(`/manager/users/api/teacher/`)
      .then(res => res.json())
      .then(data => {
        for(const item of data.data){
          $('#id_teacher').append($('<option>', { value: item.pk, text: item.fullname }))
          $('#id_group').append($('<option>', { value: item.group_pk, text: item.group_name }))
        }
      })
  }

  function addGroupForm() {
    const textHtml = `
      <div class="col-12 col-md-6">
      <label>Старт</label>
      <input 
        placeholder="Например, c 2023-02-06" 
        name="date_start"
        type="text" id="fp-range" 
        class="form-control flatpickr-basic flatpickr-input active select2" required>
      </div>
      <div class="col-12 col-md-6">
        <label>Название группы [Номер]</label>
        <input required="" placeholder="Например, Группа 4221"  name="group_name" type="text" id="fp-time" class="form-control" required>
      </div>`
    
    document.querySelector('#bottomModalElement').insertAdjacentHTML('afterend', textHtml)
  }

  $('#addGropuBtn').click(() => {
    addGroupForm()
    getAllTeacher()
  })
    
})
