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
    const fields = [
      'IGS_ID','SiteName','Latitude_deg','Longitude_deg','Ellipsoidal_height_m','Monument_type','Antenna_model','Antenna_serial','Antenna_height_m','Receiver_model','Obs_start_date','Obs_last_date','Obs_span_yr','Data_availability_count','Processed_count','Not_estimated_count','Repeatability_N_mm','Repeatability_E_mm','Repeatability_U_mm','Velocity_N_mm_per_yr','Velocity_E_mm_per_yr','Velocity_U_mm_per_yr','Discontinuities_notes','Regional_consistency_flag','DOMES_number','Data_transfer_method','Archive_centres','SiteLog_URL','Site_photos_URLs','Operator_institution','Contact_email','Commitment_3yr','AnnexA_plot_path','Status_recommendation','Notes_action_items'
    ]
    fields.forEach(f => {
      const tr = document.createElement('tr')
      const th = document.createElement('th')
      // present human-friendly header and units for velocity fields
      let displayName = f
      let unit = ''
      if (f.startsWith('Velocity_')) {
        // e.g. 'Velocity_N_mm_per_yr' -> 'Velocity N' with unit 'mm/yr'
        const parts = f.split('_')
        // parts[1] = N/E/U
        displayName = `Velocity ${parts[1]}`
        unit = 'mm/yr'
      }
      th.textContent = displayName + (unit ? ' (' + unit + ')' : '')
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
