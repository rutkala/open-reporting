#!/bin/bash
SITES=(
  #"https://data.europa.eu/apps/data-visualisation-guide/"
  #"https://ibcs.com"
  #"https://github.com/UrbanInstitute/graphics-styleguide"
  #"https://m2.material.io/design/communication/data-visualization.html"
  #"https://playfairdata.com"
  #"https://datavizstyleguide.com"
  #"https://scientificdiscovery.dev"
  #"https://hype4.academy/learn"
  #"https://www.justinmind.com"
  "https://www.justinmind.com/ui-design"
  "https://www.justinmind.com/ux-design"
  "https://www.justinmind.com/ui-design/dashboard-design-best-practices-ux"
)
mkdir -p viz-kb-full
cd viz-kb-full
for site in "${SITES[@]}"; do
  echo "Mirroring $site..."
  wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
       --accept html,pdf,png,jpg,jpeg,svg,webp,gif,css,js --level=3 --wait=2 --random-wait \
       -P "$(basename ${site%%/*})" "$site" || echo "Partial/failed: $site"
done
# Git clones separately
#git clone https://github.com/UrbanInstitute/graphics-styleguide.git
#find . -name "*.pdf" -exec echo "PDF found: {}" \;
#echo "Full KB in viz-kb-full/. Zip and upload to Claude."