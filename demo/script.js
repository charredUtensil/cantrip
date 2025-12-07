function main() {
  const checkboxes = document.querySelectorAll(
    'input[name="font-feature"]'
  );

  function updateFontFeatureSettings() {
    checkboxes.forEach(cb => {
      document.body.style.setProperty(
        `--font-feature-${cb.value}`,
        `${cb.checked ? 1 : 0}`
      );
    });
  }

  checkboxes.forEach((cb) => {
    cb.addEventListener("change", updateFontFeatureSettings);
  });

  updateFontFeatureSettings();
}

if (document.readyState != 'loading'){
  main();
} else {
  document.addEventListener('DOMContentLoaded', main);
}