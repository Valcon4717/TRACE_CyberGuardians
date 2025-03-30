import { Tooltip as TooltipPrimitive } from "bits-ui";
import Content from "./tooltip-content.svelte";

const Root = TooltipPrimitive.Root;
const Trigger = TooltipPrimitive.Trigger;
const Provider = TooltipPrimitive.Provider;

export {
	Root,
	Trigger,
	Content,
	Provider as TooltipProvider,
	//
	Root as Tooltip,
	Trigger as TooltipTrigger,
	Content as TooltipContent
};
