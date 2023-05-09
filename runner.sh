USE_POETRY=false
if [ "$1" = "-y" ]; then
  USE_POETRY=true
  shift  # shift the '-y' argument off the argument list
fi

ARGS="$@"
if [ -z "$ARGS" ]; then
  ARGS=""
fi

if [ "$USE_POETRY" = true ]; then
  COMMAND="poetry run app $ARGS"
else
  COMMAND="python3 -m src.kault.kault $ARGS"
fi

eval "$COMMAND"
