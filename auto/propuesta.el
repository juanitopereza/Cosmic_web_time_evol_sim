(TeX-add-style-hook "propuesta"
 (lambda ()
    (LaTeX-add-bibitems
     "Gadget"
     "Forero-Romero"
     "tv-web")
    (TeX-run-style-hooks
     "amsmath"
     "inputenc"
     "utf8"
     "latex2e"
     "art10"
     "article"
     "")))

