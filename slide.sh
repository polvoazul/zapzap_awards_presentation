#!/bin/bash
jupyter nbconvert 3_analysis.ipynb \
    --reveal-prefix=https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0 \
    --SlidesExporter.reveal_scroll=True \
    --to slides \
    --output `python -c "import settings; print(settings.GROUP_NAME)"`

