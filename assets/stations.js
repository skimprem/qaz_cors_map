document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('table-container')
  // Use relative path so page works via file:// or simple HTTP server
  fetch('data/web/candidates.json')
    .then(r => {
      if (!r.ok) throw new Error('HTTP ' + r.status)
      return r.json()
    })
    .then(data => renderTable(data))
    .catch(e => { container.innerText = 'Failed to load data (run scripts/generate_web_assets.py first or serve via HTTP)'; console.error(e) })

  function renderTable(rows) {
    const table = document.createElement('table')
    table.className = 'candidates'
    const thead = document.createElement('thead')
    thead.innerHTML = '<tr><th>ID</th><th>First</th><th>Last</th><th>Span (yr)</th><th>Available</th><th>Processed</th><th>Not estimated</th><th>Preview</th></tr>'
    table.appendChild(thead)
    const tbody = document.createElement('tbody')
    rows.forEach(r => {
      const tr = document.createElement('tr')
      // make Site clickable to toggle details
      tr.innerHTML = `<td class="site-cell"><a href="#" class="site-link">${r.Site}</a></td><td>${r.First_obs}</td><td>${r.Last_obs}</td><td>${r.Span_yr}</td><td>${r.Available}</td><td>${r.Processed}</td><td>${r.Not_estimated}</td>`
      const tdPreview = document.createElement('td')
      const imgPath = `data/web/station_images/${r.Site}.png`
      const pdfPath = `data/stations/${r.Site}.pdf`
      const btn = document.createElement('button')
      btn.textContent = 'View'
      btn.addEventListener('click', () => openModal(imgPath, pdfPath))
      tdPreview.appendChild(btn)
      tr.appendChild(tdPreview)
      tbody.appendChild(tr)
      // attach toggle for details
      const siteLink = tr.querySelector('.site-link')
      siteLink.addEventListener('click', (ev) => {
        ev.preventDefault()
        toggleDetailsRow(tr, r)
      })
    })
    table.appendChild(tbody)
    container.appendChild(table)

    openRequestedSite(tbody)
  }

  // if the page was opened as stations.html?site=EIND (e.g. from a map
  // marker's popup link), expand and scroll to that station's row
  function openRequestedSite(tbody) {
    const wanted = (new URLSearchParams(window.location.search).get('site') || '').trim().toUpperCase()
    if (!wanted) return
    const siteLink = Array.from(tbody.querySelectorAll('.site-link'))
      .find(a => a.textContent.trim().toUpperCase() === wanted)
    if (!siteLink) return
    siteLink.click()
    const tr = siteLink.closest('tr')
    tr.classList.add('highlighted')
    tr.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }

  const modal = document.getElementById('modal')
  const modalImg = document.getElementById('modal-img')
  const modalClose = document.getElementById('modal-close')
  modalClose.addEventListener('click', closeModal)

  function openModal(img, pdf) {
    modalImg.src = img
    modal.classList.remove('hidden')
  }
  function closeModal() {
    modal.classList.add('hidden')
    modalImg.src = ''
  }

  // create or remove a details row after the given row
  function toggleDetailsRow(row, record) {
    // if next sibling is a details row, remove it
    const next = row.nextElementSibling
    if (next && next.classList.contains('details-row')) {
      next.remove()
      return
    }
    // otherwise build details tr
    const cols = row.querySelectorAll('td').length
    const detailsTr = document.createElement('tr')
    detailsTr.className = 'details-row'
    const td = document.createElement('td')
    td.colSpan = cols
    // build inner table of selected fields
    const detailTable = document.createElement('table')
    detailTable.className = 'detail-table'
    // [record key, display label]; date/count fields already shown in the
    // main table (First_obs, Last_obs, Span_yr, Available, Processed,
    // Not_estimated) are intentionally left out here to avoid duplication
    const fields = [
      ['IGS_ID', 'IGS ID'], ['SiteName', 'Site Name'],
      ['Latitude_deg', 'Latitude (deg)'], ['Longitude_deg', 'Longitude (deg)'],
      ['Ellipsoidal_height_m', 'Ellipsoidal height (m)'], ['Monument_type', 'Monument type'],
      ['Antenna_model', 'Antenna model'], ['Antenna_serial', 'Antenna serial'],
      ['Antenna_height_m', 'Antenna height (m)'], ['Receiver_model', 'Receiver model'],
      ['Repeatability_N_mm', 'Repeatability N (mm)'], ['Repeatability_E_mm', 'Repeatability E (mm)'],
      ['Repeatability_U_mm', 'Repeatability U (mm)'],
      ['Velocity_N_mm_per_yr', 'Velocity N'], ['Velocity_E_mm_per_yr', 'Velocity E'],
      ['Velocity_U_mm_per_yr', 'Velocity U'],
      ['Discontinuities_notes', 'Discontinuities notes'], ['Regional_consistency_flag', 'Regional consistency flag'],
      ['DOMES_number', 'DOMES number'], ['Data_transfer_method', 'Data transfer method'],
      ['Archive_centres', 'Archive centres'], ['SiteLog_URL', 'SiteLog URL'],
      ['Site_photos_URLs', 'Site photos URLs'], ['Operator_institution', 'Operator institution'],
      ['Contact_email', 'Contact email'], ['Commitment_3yr', 'Commitment 3yr'],
      ['AnnexA_plot_path', 'AnnexA plot path'], ['Status_recommendation', 'Status recommendation'],
      ['Notes_action_items', 'Notes action items'],
    ]
    fields.forEach(([f, label]) => {
      const tr = document.createElement('tr')
      const th = document.createElement('th')
      // present units alongside velocity fields
      const unit = f.startsWith('Velocity_') ? 'mm/yr' : ''
      th.textContent = label + (unit ? ' (' + unit + ')' : '')
      const val = document.createElement('td')
      // use value from record if present, otherwise blank
      // show uncertainties next to velocity fields if available
      if (f.startsWith('Velocity_')) {
        const base = record[f] !== undefined && record[f] !== null ? record[f] : ''
        const uncField = f.replace(/_mm_per_yr$/, '') + '_uncertainty_mm_per_yr'
        const unc = record[uncField]
        if (base && unc) {
          val.textContent = base + ' ± ' + unc
        } else if (base) {
          val.textContent = base
        } else {
          val.textContent = ''
        }
      } else {
        val.textContent = record[f] !== undefined && record[f] !== null ? record[f] : ''
      }
      // if AnnexA_plot_path, create link
      if (f === 'AnnexA_plot_path' && val.textContent) {
        const a = document.createElement('a')
        a.href = val.textContent
        a.target = '_blank'
        a.textContent = 'Open plot'
        val.textContent = ''
        val.appendChild(a)
      }
      if (f === 'Site_photos_URLs' && val.textContent) {
        // assume comma-separated urls
        const urls = String(val.textContent).split(/[,;]\s*/)
        val.textContent = ''
        urls.forEach(u => {
          const a = document.createElement('a')
          a.href = u
          a.target = '_blank'
          a.textContent = 'photo'
          a.style.marginRight = '6px'
          val.appendChild(a)
        })
      }
      tr.appendChild(th)
      tr.appendChild(val)
      detailTable.appendChild(tr)
    })
    td.appendChild(detailTable)
    detailsTr.appendChild(td)
    // insert after row
    row.parentNode.insertBefore(detailsTr, row.nextSibling)
  }
})
