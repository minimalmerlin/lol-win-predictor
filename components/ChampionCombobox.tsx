'use client';

import * as React from 'react';
import { Check, ChevronsUpDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { api } from '@/lib/api';

interface ChampionComboboxProps {
  onSelect: (champion: string) => void;
  disabled?: boolean;
}

export default function ChampionCombobox({ onSelect, disabled }: ChampionComboboxProps) {
  const [open, setOpen] = React.useState(false);
  const [value, setValue] = React.useState('');
  const [champions, setChampions] = React.useState<string[]>([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchChampions = async () => {
      try {
        const data = await api.getChampionsList();
        setChampions(data);
      } catch (error) {
        console.error('Failed to fetch champions:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchChampions();
  }, []);

  const handleSelect = (currentValue: string) => {
    const selected = champions.find(
      (champ) => champ.toLowerCase() === currentValue.toLowerCase()
    );
    if (selected) {
      onSelect(selected);
      setValue('');
      setOpen(false);
    }
  };

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between bg-slate-700/50 border-slate-600 text-white hover:bg-slate-700 hover:text-white"
          disabled={disabled || loading}
        >
          {loading ? 'Loading champions...' : 'Select champion...'}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0 bg-slate-800 border-slate-600">
        <Command className="bg-slate-800">
          <CommandInput
            placeholder="Search champion..."
            className="border-0 bg-slate-700 text-white placeholder:text-slate-400"
          />
          <CommandList>
            <CommandEmpty className="text-slate-400">No champion found.</CommandEmpty>
            <CommandGroup>
              {champions.map((champion) => (
                <CommandItem
                  key={champion}
                  value={champion}
                  onSelect={handleSelect}
                  className="text-white hover:bg-slate-700 cursor-pointer"
                >
                  <Check
                    className={cn(
                      'mr-2 h-4 w-4',
                      value === champion.toLowerCase() ? 'opacity-100' : 'opacity-0'
                    )}
                  />
                  {champion}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
