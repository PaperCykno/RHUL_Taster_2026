async function loadArchiveIndex() {
  try {
    const response = await fetch(
      "/archive/data/site-index.json"
    );

    const data = await response.json();

    window.archiveIndex = data;
  } catch (error) {
    console.debug(
      "Archived index unavailable",
      error
    );
  }
}

loadArchiveIndex();