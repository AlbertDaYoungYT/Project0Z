-- static/assets/lua/effects/poison.lua
local Effect = require("core.effect") -- Assuming Lua's require can find 'core.effect.lua'

local Poison = Effect:new({
  name = "Poison",
  duration = 10, -- Example property
  tick_rate = 5
})

function Poison:on_tick(infected_player_proxy)
  -- infected_player_proxy is an object/table passed from Python,
  -- exposing methods Python wants Lua to be able to call.
  if infected_player_proxy and infected_player_proxy.hurt then
    infected_player_proxy:hurt(10.0)
  else
    log_info("Lua Poison Error: infected_player_proxy or hurt method missing")
  end
end


-- Or, more simply, the Python loader might expect this file to return the asset.
return Poison
