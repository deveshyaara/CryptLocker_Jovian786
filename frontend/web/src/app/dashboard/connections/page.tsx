import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { ListFilter, MoreVertical, PlusCircle, Search } from "lucide-react";
import Image from "next/image";

const connections = [
  { name: 'MIT', type: 'Issuer', date: 'Jan 10, 2024', status: 'Active', logoUrl: 'https://picsum.photos/seed/101/40/40' },
  { name: 'Tech Corp', type: 'Verifier', date: 'Feb 28, 2023', status: 'Active', logoUrl: 'https://picsum.photos/seed/102/40/40' },
  { name: 'GovPortal', type: 'Issuer/Verifier', date: 'Jun 15, 2022', status: 'Active', logoUrl: 'https://picsum.photos/seed/103/40/40' },
  { name: 'SocialApp', type: 'Verifier', date: 'May 05, 2024', status: 'Pending', logoUrl: 'https://picsum.photos/seed/105/40/40' },
  { name: 'Old Company', type: 'Issuer', date: 'Nov 1, 2021', status: 'Inactive', logoUrl: 'https://picsum.photos/seed/106/40/40' },
];

export default function ConnectionsPage() {
    return (
        <div className="flex flex-col h-full">
            <header className="flex items-center gap-4 mb-6">
                <h1 className="text-3xl font-bold font-headline">My Connections</h1>
                <div className="ml-auto flex items-center gap-2">
                    <Button className="gap-1">
                        <PlusCircle className="h-3.5 w-3.5" />
                        <span>Add Connection</span>
                    </Button>
                </div>
            </header>
            
            <div className="flex items-center gap-4 mb-4">
                <div className="relative flex-1">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input placeholder="Search by organization..." className="pl-8" />
                </div>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="outline" className="gap-1">
                            <ListFilter className="h-3.5 w-3.5" />
                            <span>Filter</span>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Filter by Status</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuCheckboxItem checked>All</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>Active</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>Pending</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>Inactive</DropdownMenuCheckboxItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {connections.map((conn, index) => (
                    <Card key={index}>
                        <CardHeader className="flex flex-row items-center gap-4">
                             <Image src={conn.logoUrl} alt={`${conn.name} logo`} width={48} height={48} className="rounded-lg" data-ai-hint="company logo" />
                            <div className="flex-1">
                                <CardTitle>{conn.name}</CardTitle>
                                <CardDescription>{conn.type}</CardDescription>
                            </div>
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button size="icon" variant="ghost">
                                        <MoreVertical className="h-4 w-4" />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end">
                                    <DropdownMenuItem>View Details</DropdownMenuItem>
                                    <DropdownMenuItem className="text-destructive focus:bg-destructive/10 focus:text-destructive">Disconnect</DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </CardHeader>
                        <CardContent>
                           <div className="flex justify-between text-sm text-muted-foreground">
                                <span>Connected on {conn.date}</span>
                                <span className={`font-semibold ${
                                    conn.status === 'Active' ? 'text-accent' : 
                                    conn.status === 'Pending' ? 'text-yellow-500' : 'text-muted-foreground'
                                }`}>{conn.status}</span>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
