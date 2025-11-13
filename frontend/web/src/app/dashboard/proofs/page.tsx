import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ShieldAlert } from "lucide-react";

export default function ProofsPage() {
    return (
        <div className="flex flex-col h-full">
            <header className="flex items-center gap-4 mb-6">
                <h1 className="text-3xl font-bold font-headline">Proof Requests</h1>
            </header>
            
            <div className="flex flex-1 items-center justify-center rounded-lg border border-dashed shadow-sm">
                <div className="flex flex-col items-center gap-2 text-center">
                    <ShieldAlert className="h-12 w-12 text-muted-foreground" />
                    <h3 className="text-2xl font-bold tracking-tight">No Pending Proof Requests</h3>
                    <p className="text-sm text-muted-foreground">When a service requests information, it will appear here.</p>
                </div>
            </div>
        </div>
    );
}
