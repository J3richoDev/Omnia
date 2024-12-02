const themeToggle = document.getElementById('theme-toggle');
        const currentTheme = localStorage.getItem('theme');

        if (currentTheme) {
            document.documentElement.setAttribute('data-theme', currentTheme);
            themeToggle.checked = currentTheme === 'light';
        }

        themeToggle.addEventListener('change', () => {
            const newTheme = themeToggle.checked ? 'light' : 'night';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });