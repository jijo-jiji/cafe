/**
 * CAFE HRMS - Main Interactive JavaScript
 * Provides live clock, table search & filtering, dynamic leave day calculations,
 * wage estimator, and modal confirmation handlers.
 */

document.addEventListener('DOMContentLoaded', () => {
  initLiveClock();
  initTableSearch();
  initLeaveDaysCalculator();
  initWageEstimator();
  initAlertDismissal();
  initModalConfirmations();
});

/* ==========================================================================
   1. Live Digital Clock & Real-time Date
   ========================================================================== */
function initLiveClock() {
  const clockElement = document.getElementById('live-clock-display');
  const dateElement = document.getElementById('live-date-display');
  if (!clockElement && !dateElement) return;

  function updateTime() {
    const now = new Date();
    
    if (clockElement) {
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      clockElement.textContent = `${hours}:${minutes}:${seconds}`;
    }

    if (dateElement) {
      const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
      dateElement.textContent = now.toLocaleDateString(undefined, options);
    }
  }

  updateTime();
  setInterval(updateTime, 1000);
}

/* ==========================================================================
   2. Instant Table Search & Filter
   ========================================================================== */
function initTableSearch() {
  const searchInputs = document.querySelectorAll('[data-table-search]');
  
  searchInputs.forEach(input => {
    const tableId = input.getAttribute('data-table-search');
    const table = document.getElementById(tableId) || document.querySelector('.custom-table');
    if (!table) return;

    input.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase().trim();
      const rows = table.querySelectorAll('tbody tr:not(.no-filter)');

      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(term)) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   3. Dynamic Leave Day & Balance Calculator
   ========================================================================== */
function initLeaveDaysCalculator() {
  const startDateInput = document.querySelector('input[name="start_date"]') || document.getElementById('id_start_date');
  const endDateInput = document.querySelector('input[name="end_date"]') || document.getElementById('id_end_date');
  const previewBox = document.getElementById('leave-calculation-preview');
  const daysDisplay = document.getElementById('calc-total-days');
  const remainingDisplay = document.getElementById('calc-remaining-balance');

  if (!startDateInput || !endDateInput || !previewBox) return;

  const currentBalance = parseInt(previewBox.getAttribute('data-current-balance') || '14', 10);

  function calculateDays() {
    const startVal = startDateInput.value;
    const endVal = endDateInput.value;

    if (!startVal || !endVal) {
      previewBox.style.display = 'none';
      return;
    }

    const start = new Date(startVal);
    const end = new Date(endVal);

    if (end < start) {
      previewBox.style.display = 'block';
      if (daysDisplay) daysDisplay.textContent = 'Invalid (End date cannot be before start date)';
      if (remainingDisplay) remainingDisplay.textContent = '-';
      previewBox.style.borderColor = 'var(--status-danger-border)';
      previewBox.style.background = 'var(--status-danger-bg)';
      return;
    }

    // Calculation: Difference in days inclusive (+1)
    const diffTime = Math.abs(end - start);
    const totalDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    const remaining = currentBalance - totalDays;

    previewBox.style.display = 'block';
    if (daysDisplay) daysDisplay.textContent = `${totalDays} Day${totalDays > 1 ? 's' : ''}`;
    
    if (remainingDisplay) {
      remainingDisplay.textContent = `${remaining} Day${remaining !== 1 ? 's' : ''}`;
      if (remaining < 0) {
        remainingDisplay.textContent += ' (Exceeds available balance!)';
        previewBox.style.borderColor = 'var(--status-danger-border)';
        previewBox.style.background = 'var(--status-danger-bg)';
      } else {
        previewBox.style.borderColor = '#f3deb9';
        previewBox.style.background = 'linear-gradient(135deg, #fef8ee 0%, #faf3e8 100%)';
      }
    }
  }

  startDateInput.addEventListener('change', calculateDays);
  endDateInput.addEventListener('change', calculateDays);
}

/* ==========================================================================
   4. Interactive Wage & Payroll Estimator
   ========================================================================== */
function initWageEstimator() {
  const hoursInput = document.getElementById('calc-input-hours');
  const rateInput = document.getElementById('calc-input-rate');
  const otInput = document.getElementById('calc-input-ot');
  
  const basePayDisplay = document.getElementById('calc-result-base');
  const otPayDisplay = document.getElementById('calc-result-ot');
  const totalGrossDisplay = document.getElementById('calc-result-total');

  if (!hoursInput || !rateInput) return;

  function recalculate() {
    const hours = parseFloat(hoursInput.value) || 0;
    const rate = parseFloat(rateInput.value) || 0;
    const otHours = parseFloat(otInput ? otInput.value : 0) || 0;

    const basePay = hours * rate;
    const otPay = otHours * (rate * 1.5);
    const totalGross = basePay + otPay;

    if (basePayDisplay) basePayDisplay.textContent = `RM ${basePay.toFixed(2)}`;
    if (otPayDisplay) otPayDisplay.textContent = `RM ${otPay.toFixed(2)}`;
    if (totalGrossDisplay) totalGrossDisplay.textContent = `RM ${totalGross.toFixed(2)}`;
  }

  hoursInput.addEventListener('input', recalculate);
  rateInput.addEventListener('input', recalculate);
  if (otInput) otInput.addEventListener('input', recalculate);
}

/* ==========================================================================
   5. Alert Auto-Dismissal
   ========================================================================== */
function initAlertDismissal() {
  const alerts = document.querySelectorAll('.alert');
  
  alerts.forEach(alert => {
    // Auto fade after 5 seconds
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 400);
    }, 5000);

    const closeBtn = alert.querySelector('.alert-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        alert.remove();
      });
    }
  });
}

/* ==========================================================================
   6. Modal Confirmation Dialogs
   ========================================================================== */
function initModalConfirmations() {
  const modalOverlay = document.getElementById('confirmation-modal');
  const modalForm = document.getElementById('confirm-modal-form');
  const modalTitle = document.getElementById('confirm-modal-title');
  const modalText = document.getElementById('confirm-modal-text');
  const cancelBtn = document.getElementById('confirm-modal-cancel');

  if (!modalOverlay) return;

  document.querySelectorAll('[data-confirm-action]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const actionUrl = btn.getAttribute('data-confirm-action');
      const title = btn.getAttribute('data-confirm-title') || 'Are you sure?';
      const text = btn.getAttribute('data-confirm-text') || 'Do you want to proceed with this action?';

      if (modalTitle) modalTitle.textContent = title;
      if (modalText) modalText.textContent = text;
      if (modalForm) modalForm.action = actionUrl;

      modalOverlay.classList.add('active');
    });
  });

  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
    });
  }

  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
      modalOverlay.classList.remove('active');
    }
  });
}
