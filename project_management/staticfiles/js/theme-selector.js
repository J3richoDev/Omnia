const themeToggle = document.getElementById('theme-toggle');
        const currentTheme = localStorage.getItem('theme');

        if (currentTheme) {
            document.documentElement.setAttribute('data-theme', currentTheme);
            themeToggle.checked = currentTheme === 'night';
        }

        themeToggle.addEventListener('change', () => {
            const newTheme = themeToggle.checked ? 'night' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });