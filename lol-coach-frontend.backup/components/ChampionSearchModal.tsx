'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Search } from 'lucide-react';
import ChampionSearch from './ChampionSearch';

export default function ChampionSearchModal() {
  const [open, setOpen] = useState(false);
  const router = useRouter();

  const handleChampionSelect = (championId: string) => {
    setOpen(false);
    router.push(`/champions/${championId}`);
  };

  return (
    <>
      <Button
        variant="outline"
        onClick={() => setOpen(true)}
        className="relative overflow-hidden group border-primary/20 hover:border-primary/40 hover:bg-primary/5"
      >
        <Search className="mr-2 h-4 w-4" />
        <span>Champion suchen</span>
        <div className="absolute inset-0 shimmer" />
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-2xl glass border-primary/20">
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Champion Search
            </DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <ChampionSearch onSelect={handleChampionSelect} />
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
