window.addEventListener('load', () => {

  function getTheadCheckBox() {
    return document.getElementById('checkboxSelectAll')
  }

  function getTableCheckBox() {
    return document.querySelectorAll('.form-check-input')
  }

  const targetElement = getTheadCheckBox()

  if (targetElement) {
    targetElement.addEventListener('click' , (event) => {

      for (const el of [...getTableCheckBox()].slice(1)) {
        el.click()
      }
    })
  }

})