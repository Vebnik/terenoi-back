window.addEventListener('load', () => {

  const target_select = document.querySelector('#paginate_by')
  let def_value = document.cookie.split(';')[0].match(/(\d+)/mi)[0]

  if (target_select) {
    if (def_value === '5') {
      def_value = 10
      document.cookie = `paginate_by=${def_value}`
    }

    target_select.value = def_value

    target_select.addEventListener('change', (event) => {
      document.cookie = `paginate_by=${target_select.value}`
      window.open(`${window.location.pathname}`, target='_self')
    })
  }
})