-- static/assets/lua/core/quest.lua
local Quest = {}
Quest.__index = Quest

Quest.STATUS = {
  NOT_STARTED = "not_started",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed", -- Objectives met, ready to turn in
  TURNED_IN = "turned_in"  -- Rewards given
}

function Quest:new(o)
  o = o or {}
  o.id = o.id or "quest_" .. string.gsub(o.title or "untitled", "%s+", "_"):lower() .. "_" .. tostring(math.random(10000))
  o.title = o.title or "Untitled Quest"
  o.description = o.description or "No description provided."
  o.giver_id = o.giver_id or nil -- ID of the NPC or entity that gives the quest
  o.turn_in_id = o.turn_in_id or o.giver_id -- ID of the NPC or entity to turn the quest into
  o.asset_type = "quest" -- For registration
  
  o.objectives = o.objectives or {} 
  -- Example objective structure:
  -- { 
  --   { id="obj1", type="kill", target_key="monster_goblin", current_count=0, required_count=5, description="Slay 5 Goblins", completed=false },
  --   { id="obj2", type="collect", item_key="item_rare_herb", current_count=0, required_count=3, description="Collect 3 Rare Herbs", completed=false },
  --   { id="obj3", type="reach_location", location_key="loc_ancient_ruins", description="Find the Ancient Ruins", completed=false }
  -- }
  
  o.rewards = o.rewards or {
    experience = 0,
    currency = {}, -- e.g. { gold = 100, silver = 50 }
    items = {} -- list of item keys or { item_key="key", count=1 }
  }
  
  o.status = o.status or Quest.STATUS.NOT_STARTED
  o.is_repeatable = o.is_repeatable or false

  setmetatable(o, self)
  return o
end

-- Called when a player accepts the quest
-- player_proxy: proxy for the player
function Quest:on_accept(player_proxy)
  if self.status == Quest.STATUS.NOT_STARTED then
    self.status = Quest.STATUS.IN_PROGRESS
    log_info("Lua Quest: '" .. self.title .. "' accepted by " .. (player_proxy and player_proxy.name or "player"))
    -- Potentially register for game events related to objectives via Python bridge
    return true
  end
  return false
end

-- Update progress for a specific objective by its ID
-- player_proxy: proxy for the player
-- objective_id: string, the ID of the objective to update
-- progress_data: table, data relevant to the objective type (e.g., { count_increase = 1 } or { completed = true })
function Quest:update_objective_progress(player_proxy, objective_id, progress_data)
  if self.status ~= Quest.STATUS.IN_PROGRESS then return false end
  
  local objective_updated = false
  for _, objective in ipairs(self.objectives) do
    if objective.id == objective_id and not objective.completed then
      -- log_info("Lua Quest: Updating objective '" .. (objective.description or objective_id) .. "' for quest '" .. self.title .. "'")
      if (objective.type == "kill" or objective.type == "collect") and progress_data.count_increase then
        objective.current_count = math.min((objective.current_count or 0) + progress_data.count_increase, objective.required_count)
        if objective.current_count >= objective.required_count then objective.completed = true end
      elseif objective.type == "reach_location" and progress_data.completed then
         objective.completed = true
      end
      -- Add more objective type handling as needed
      objective_updated = true
      break
    end
  end

  if objective_updated then self:_check_completion(player_proxy) end
  return objective_updated
end

-- Check if all objectives are met
function Quest:_check_completion(player_proxy)
  if self.status ~= Quest.STATUS.IN_PROGRESS then return end
  local all_objectives_met = true
  for _, objective in ipairs(self.objectives) do
    if not objective.completed then all_objectives_met = false; break end
  end

  if all_objectives_met then
    self.status = Quest.STATUS.COMPLETED
    log_info("Lua Quest: All objectives for '" .. self.title .. "' completed. Ready to turn in.")
    -- if self._on_objectives_completed then self:_on_objectives_completed(player_proxy) end
  end
end

-- Called when the player attempts to turn in the quest
function Quest:on_turn_in(player_proxy)
  if self.status == Quest.STATUS.COMPLETED then
    self.status = Quest.STATUS.TURNED_IN
    log_info("Lua Quest: '" .. self.title .. "' turned in by " .. (player_proxy and player_proxy.name or "player") .. ". Rewards to be granted.")
    -- Grant rewards to player_proxy (this would likely involve calls to Python/game systems)
    -- if self._on_rewards_given then self:_on_rewards_given(player_proxy) end
    return true
  else
    log_info("Lua Quest: '" .. self.title .. "' cannot be turned in. Status: " .. self.status)
    return false
  end
end

return Quest