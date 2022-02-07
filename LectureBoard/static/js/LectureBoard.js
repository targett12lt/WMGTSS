$(function() {
  let pdfDoc = null,
      pageNum = 1,
      pageRendering = false,
      pageNumPending = null;

  const scale = 5.0,
        canvas = document.getElementById('pdf-canvas'),
        pnum = document.getElementById('page-num')
        ctx = canvas.getContext('2d');
  /**
   * Gets page info from document, resizes the canvas accordingly and renders page
   * @param num Page number.
   */
  function renderPage(num) {
    pageRendering = true;
    
    // Using promise to fetch the page
    pdfDoc.getPage(num).then(function(page) {
      const page_viewport = page.getViewport(scale);
      canvas.height = page_viewport.height;
      canvas.width = page_viewport.width;

      // Render PDF page into canvas context
      const renderContext = {
        canvasContext: ctx,
        viewport: page_viewport
      };
      const renderTask = page.render(renderContext);

      // Wait for rendering to finish
      renderTask.promise.then(function() {
        pageRendering = false;
        if (pageNumPending !== null) {
          // New page rendering is pending
          renderPage(pageNumPending);
          pageNumPending = null;
        }
      });
    });

    // Update page counters
    $(pnum).text(num);
  }

  /**
   * If another page rendering in progress, waits until the rendering is
   * finised. Otherwise, executes rendering immediately.
   */
  function queueRenderPage(num) {
    if (pageRendering) {
      pageNumPending = num;
    } else {
      renderPage(num);
    }
  }

  /**
   * Displays the previous page:
   */
  $(".carousel-control-prev").click(function() {
    if (pageNum > 1) {
      pageNum--;
      queueRenderPage(pageNum);
    }
  });

  /**
   * Displays the next page:
   */
  $(".carousel-control-next").click(function() {
    if (pageNum < pdfDoc.numPages) {
      pageNum++;
      queueRenderPage(pageNum);
    }
  });

  /**
   * Getting the PDF File from the DataBase Storage System:
   */
  $(function() {
    const url = $(canvas).data("file");
    pdfjsLib.getDocument(url).then(function(pdfDoc_) {
      pdfDoc = pdfDoc_;
      $("#page-count").text(pdfDoc.numPages);

      // Initial page rendering:
      renderPage(pageNum);
    });
  });
  /**
   * Prints hello world in a message box - FOR TESTING PURPOSES
   */
  (function myFunction() {
    alert("Hello world!")
  });
});