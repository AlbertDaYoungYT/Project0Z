-- static/assets/lua/effects/regeneration.lua
local Effect = require("core.effect") -- Assuming Lua's require can find 'core.effect.lua'

local Regeneration = Effect:new({
  name = "Regeneration",
  duration = 10, -- Example property
  tick_rate = 1
})

function Regeneration:on_tick(infected_player_proxy)
  -- infected_player_proxy is an object/table passed from Python,
  -- exposing methods Python wants Lua to be able to call.
  if infected_player_proxy and infected_player_proxy.add_health then
    infected_player_proxy:add_health(10.0)
    -- print("Lua Regeneration: Healed player by 10")
  else
    print("Lua Regeneration Error: infected_player_proxy or add_health method missing")
  end
  -- Call base if needed, though in Lua it's often explicit
  -- Effect._on_tick(self, infected_player_proxy)
end

-- Registration:
-- This depends on how you set up the Python-Lua bridge.
-- Example: If Python exposed `server.register_effect(name, effect_table)`
-- server.register_effect("Regeneration", Regeneration)

-- Or, more simply, the Python loader might expect this file to return the asset.
return Regeneration
