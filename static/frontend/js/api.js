const API = {
    getLeads: () => fetch('/api/leads/').then(r => r.json()),
    getBookings: () => fetch('/api/bookings/').then(r => r.json()),
    getDashboard: () => fetch('/api/dashboard-stats/').then(r => r.json()),
};