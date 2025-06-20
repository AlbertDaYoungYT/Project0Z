-- static/assets_lua/core/effect.lua
local Effect = {}
Effect.__index = Effect

function Effect:new(o)
  o = o or {}
  setmetatable(o, self)
  return o
end

function Effect:on_tick(infected_player_proxy)
  error("Effect:on_tick must be implemented by subclass")
end

function Effect:on_applied(infected_player_proxy)
  -- Default implementation (optional)
end

function Effect:while_applied(infected_player_proxy)
  -- Default implementation (optional)
end

return Effect
