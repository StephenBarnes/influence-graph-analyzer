s/<edge id="[^"]*" source="\(.*\)" target="\(.*\)">/EDGE \1 \2/
s/<y:NodeLabel [^>]*>\([^><]*\)<\/y:NodeLabel>$/LABEL \1/
s/<node id="\([^"]*\)">/NODE \1/
s/<y:BorderStyle color="[^"]*" type="\([^"]*\)" width="\([^"]*\)"\/>/BORDER \1 \2/
s/^ *//
s/^<.*$//
