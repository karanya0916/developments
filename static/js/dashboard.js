// MCB Smart Construction Management System - Interactive Frontend Script

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.mcb-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  // 2. Initialize Dashboard Charts if canvas elements exist
  const statusCanvas = document.getElementById('projectStatusChart');
  if (statusCanvas && window.dashboardChartData) {
    const data = window.dashboardChartData;
    new Chart(statusCanvas, {
      type: 'doughnut',
      data: {
        labels: data.statusLabels,
        datasets: [{
          data: data.statusCounts,
          backgroundColor: ['#10b981', '#3b82f6', '#ef4444', '#f59e0b'],
          borderWidth: 2,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' }
        },
        cutout: '70%'
      }
    });
  }

  const expenseCanvas = document.getElementById('expenseCategoryChart');
  if (expenseCanvas && window.dashboardChartData) {
    const data = window.dashboardChartData;
    new Chart(expenseCanvas, {
      type: 'bar',
      data: {
        labels: data.expenseLabels,
        datasets: [{
          label: 'Expenditure (₹)',
          data: data.expenseData,
          backgroundColor: '#d97706',
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (val) { return '₹' + (val / 1000).toLocaleString() + 'k'; }
            }
          }
        }
      }
    });
  }

  const budgetVsActualCanvas = document.getElementById('budgetVsActualChart');
  if (budgetVsActualCanvas && window.dashboardChartData) {
    const data = window.dashboardChartData;
    new Chart(budgetVsActualCanvas, {
      type: 'bar',
      data: {
        labels: data.projectNames,
        datasets: [
          {
            label: 'Estimated Budget (Lakhs ₹)',
            data: data.projectBudgets,
            backgroundColor: '#1e293b',
            borderRadius: 6
          },
          {
            label: 'Actual Expenditure (Lakhs ₹)',
            data: data.projectActuals,
            backgroundColor: '#ea580c',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: 'Amount in Lakhs (₹)' }
          }
        }
      }
    });
  }

  // 3. Site Diary Dynamic Petty Expenses Table Handler
  const addExpenseBtn = document.getElementById('addPettyExpenseRowBtn');
  const expenseTableBody = document.getElementById('pettyExpensesTableBody');
  const grandTotalBadge = document.getElementById('pettyExpenseGrandTotal');

  function calculateDailyTotal() {
    if (!expenseTableBody) return;
    let total = 0;
    const amountInputs = expenseTableBody.querySelectorAll('.expense-amount-input');
    amountInputs.forEach(input => {
      const val = parseFloat(input.value) || 0;
      total += val;
    });
    if (grandTotalBadge) {
      grandTotalBadge.innerText = '₹' + total.toLocaleString('en-IN', { minimumFractionDigits: 2 });
    }
  }

  if (addExpenseBtn && expenseTableBody) {
    addExpenseBtn.addEventListener('click', function () {
      const rowCount = expenseTableBody.querySelectorAll('tr').length;
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><input type="text" name="expense_item[]" class="form-control form-control-sm" placeholder="e.g. Tea & refreshments / Nails / Transport" required></td>
        <td><input type="number" step="0.5" name="expense_amount[]" class="form-control form-control-sm expense-amount-input" placeholder="0.00" required></td>
        <td><input type="text" name="expense_paid_to[]" class="form-control form-control-sm" placeholder="Vendor / person name"></td>
        <td>
          <select name="expense_category[]" class="form-select form-select-sm">
            <option value="Food & Beverage">Food & Refreshments</option>
            <option value="Hardware">Small Hardware / Tools</option>
            <option value="Labor Assistance">Coolie / Porters</option>
            <option value="Fuel">Fuel & Generator</option>
            <option value="Transport">Local Freight / Auto</option>
            <option value="Safety & Medical">First Aid & Safety</option>
            <option value="Miscellaneous">Miscellaneous</option>
          </select>
        </td>
        <td class="text-center">
          <button type="button" class="btn btn-sm btn-outline-danger remove-expense-row-btn"><i class="bi bi-trash"></i></button>
        </td>
      `;
      expenseTableBody.appendChild(tr);

      // Bind remove event
      tr.querySelector('.remove-expense-row-btn').addEventListener('click', function () {
        tr.remove();
        calculateDailyTotal();
      });

      // Bind change event
      tr.querySelector('.expense-amount-input').addEventListener('input', calculateDailyTotal);
    });

    // Delegate input for existing rows
    expenseTableBody.addEventListener('input', function (e) {
      if (e.target.classList.contains('expense-amount-input')) {
        calculateDailyTotal();
      }
    });

    expenseTableBody.addEventListener('click', function (e) {
      if (e.target.closest('.remove-expense-row-btn')) {
        const btn = e.target.closest('.remove-expense-row-btn');
        btn.closest('tr').remove();
        calculateDailyTotal();
      }
    });
  }

  // 4. Interactive Chatbot AJAX Handler
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatMessageInput');
  const chatBox = document.getElementById('chatBox');

  if (chatForm && chatInput && chatBox) {
    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (!message) return;

      // Append User Message to UI
      const userDiv = document.createElement('div');
      userDiv.className = 'chat-bubble-user';
      userDiv.innerHTML = `<strong>You:</strong><br>${escapeHtml(message)}`;
      chatBox.appendChild(userDiv);
      chatInput.value = '';
      chatBox.scrollTop = chatBox.scrollHeight;

      // Show typing indicator
      const typingDiv = document.createElement('div');
      typingDiv.className = 'chat-bubble-ai text-muted fst-italic';
      typingDiv.id = 'aiTypingIndicator';
      typingDiv.innerHTML = '<i class="bi bi-robot me-1"></i> MCB Assistant is typing...';
      chatBox.appendChild(typingDiv);
      chatBox.scrollTop = chatBox.scrollHeight;

      // Send to API
      fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
      })
      .then(res => res.json())
      .then(data => {
        const indicator = document.getElementById('aiTypingIndicator');
        if (indicator) indicator.remove();

        if (data.success) {
          const aiDiv = document.createElement('div');
          aiDiv.className = 'chat-bubble-ai';
          aiDiv.innerHTML = `
            <div class="d-flex align-items-center mb-1 text-primary small fw-bold">
              <i class="bi bi-robot me-1"></i> MCB Smart Assistant (${data.language.toUpperCase()})
              <span class="ms-auto text-muted fw-normal">${data.timestamp}</span>
            </div>
            <div>${formatAiResponse(data.reply)}</div>
          `;
          chatBox.appendChild(aiDiv);
        } else {
          const errDiv = document.createElement('div');
          errDiv.className = 'chat-bubble-ai text-danger';
          errDiv.innerText = 'Error: ' + (data.error || 'Could not process query.');
          chatBox.appendChild(errDiv);
        }
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch(err => {
        const indicator = document.getElementById('aiTypingIndicator');
        if (indicator) indicator.remove();
        const errDiv = document.createElement('div');
        errDiv.className = 'chat-bubble-ai text-danger';
        errDiv.innerText = 'Connection error. Please try again.';
        chatBox.appendChild(errDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
      });
    });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.innerText = text;
    return div.innerHTML;
  }

  function formatAiResponse(text) {
    // Converts basic markdown like **bold**, • bullets, and newlines to HTML
    let formatted = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n• /g, '<br>• ')
      .replace(/\n/g, '<br>');
    return formatted;
  }
});
