-- static/assets/lua/core/item.lua
local Item = {}
Item.__index = Item

function Item:new(o)
  o = o or {}
  o.name = o.name or "Unknown Item"
  o.description = o.description or ""
  o.item_type = o.item_type or "generic" -- e.g., weapon, armor, consumable, quest_item
  o.rarity = o.rarity or "common"
  o.value = o.value or 0 -- monetary value
  o.stackable = o.stackable or false
  o.max_stack = o.max_stack or (o.stackable and 99 or 1)
  o.current_stack = o.current_stack or 1
  o.is_unique = o.is_unique or false -- if player can only have one
  o.asset_type = "item" -- For registration
  o.data = o.data or {} -- for any custom data specific to the item type (e.g. damage for weapon)

  setmetatable(o, self)
  return o
end

-- Called when a player picks up this item instance
-- player_proxy: proxy for the player
function Item:on_pickup(player_proxy)
  -- log_info("Lua Item: " .. self.name .. " picked up by " .. (player_proxy and player_proxy.name or "unknown player"))
  -- Default behavior, can be overridden
end

-- Called when a player drops this item instance
-- player_proxy: proxy for the player
function Item:on_drop(player_proxy)
  -- log_info("Lua Item: " .. self.name .. " dropped by " .. (player_proxy and player_proxy.name or "unknown player"))
  -- Default behavior, can be overridden
end

-- Check if the item can be equipped by the player
-- player_proxy: proxy for the player
-- slot: (optional) specific equipment slot string
function Item:can_equip(player_proxy, slot)
  -- log_info("Lua Item: Checking if " .. self.name .. " can be equipped by " .. (player_proxy and player_proxy.name or "unknown player"))
  return false -- Default: generic items cannot be equipped; override in specific item types like weapons/armor
end

-- Called when the item is equipped
-- player_proxy: proxy for the player
-- slot: specific equipment slot string
function Item:on_equip(player_proxy, slot)
  -- log_info("Lua Item: " .. self.name .. " equipped by " .. (player_proxy and player_proxy.name or "unknown player") .. " in slot " .. (slot or "any"))
  -- This should be implemented by equippable items
end

-- Called when the item is unequipped
-- player_proxy: proxy for the player
-- slot: specific equipment slot string
function Item:on_unequip(player_proxy, slot)
  -- log_info("Lua Item: " .. self.name .. " unequipped by " .. (player_proxy and player_proxy.name or "unknown player") .. " from slot " .. (slot or "any"))
  -- This should be implemented by equippable items
end

return Item