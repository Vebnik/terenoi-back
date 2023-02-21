
const tableItem = (data) => `
    <tr role="row" class="">
        <th class="sorting_disabled dt-checkboxes-cell dt-checkboxes-select-all" rowspan="1" colspan="1" style="width: 30px;" data-col="1" aria-label="">
            <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="checkboxSelectAll">
                <label class="form-check-label" for="checkboxSelectAll"></label>
            </div>
        </th>
        <td aria-colindex="1" role="cell" class="">
            <div class="media-body align-items-center" style="display: flex;">
                    <img style="border-radius: 50%; margin-right: 10px;" width="40px" height="40px" src="${data.avatar}" alt="avatar">
                <a href="#" class="font-weight-bold d-block text-nowrap"
                target="_self">
                    ${data.fullname}
                </a>
            </div>
        </td>
        <td aria-colindex="2" role="cell" class="">
            ${ data?.group?.title ? data?.group?.title : '-' }
        </td>
        <td aria-colindex="3" role="cell" class="">
            <div class="text-nowrap">
                <span class="align-text-top text-capitalize">${ 'Абонемент' }</span>
            </div>
        </td>
        <td aria-colindex="4" role="cell" class="" ${'' ? data?.balance < 2000 : 'style="color: red;"'}>
            ${data?.balance?.money_balance ? data?.balance : 0}
        </td>
        <td aria-colindex="5" role="cell" class="">
        <span class="badge text-capitalize badge-light-${data.status_color} badge-pill">
        ${data.status}
        </span>
        </td>
        <td aria-colindex="6" role="cell" class="">
            <div class="">
                <button aria-haspopup="true" aria-expanded="false" type="button"
                        class="btn dropdown-toggle btn-link dropdown-toggle-no-caret" style=" font-size: 20px;">
                    <a href="#" class="">
                        <i data-feather="edit"></i>
                    </a>
                    📝
                </button>
            </div>
        </td>
    </tr>
`

async function get(url){
    return fetch(url).then(res => res.json())
}

async function get_students(){
    const url = 'http://127.0.0.1:8000/api/manager/users/students/'

    await get(url).then(data => {
        const tableBody = document.querySelector('tbody')
        for (const student of data.results) {
            tableBody.insertAdjacentHTML('afterend', tableItem(student))
        }
    })
}


document.addEventListener('DOMContentLoaded', async (ev) => {
    switch (location.pathname) {
        case '/manager/users/teacher/':
            break;
        case '/manager/users/manager/':
            break;
        case '/manager/users/':
            await get_students()
    }
})