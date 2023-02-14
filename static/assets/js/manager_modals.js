window.addEventListener('load', () => {

  function get_teachers(date, subject, time, weekday) {
    fetch(`/manager/users/api/teacher/?date=${date}&subject=${subject}&time=${time}&weekday=${weekday}`)
        .then(res => res.json())
        .then(data => {
          [...document.querySelector('#id_teacher').children].forEach(el => el.remove())
            for(const item of data.data){
                $('#id_teacher').append($('<option>', { value: item.pk, text: item.fullname }))
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
    
})
