import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { GraduationCap, LayoutGrid, List, ListFilter, PlusCircle, Search, Share, Briefcase, FileBadge } from "lucide-react";
import Image from "next/image";
import Link from 'next/link';

const credentials = [
  {
    type: 'Education',
    icon: <GraduationCap className="h-6 w-6 text-primary" />,
    schema: 'University Degree',
    issuer: 'MIT',
    date: 'Jan 15, 2024',
    status: 'Active',
    logoUrl: 'https://picsum.photos/seed/101/40/40'
  },
  {
    type: 'Employment',
    icon: <Briefcase className="h-6 w-6 text-primary" />,
    schema: 'Employment Verification',
    issuer: 'Tech Corp',
    date: 'Mar 01, 2023',
    status: 'Active',
    logoUrl: 'https://picsum.photos/seed/102/40/40'
  },
  {
    type: 'ID',
    icon: <FileBadge className="h-6 w-6 text-primary" />,
    schema: 'National ID',
    issuer: 'Government',
    date: 'Jun 20, 2022',
    status: 'Active',
    logoUrl: 'https://picsum.photos/seed/103/40/40'
  },
    {
    type: 'Education',
    icon: <GraduationCap className="h-6 w-6 text-primary" />,
    schema: 'Online Course Certificate',
    issuer: 'Web Academy',
    date: 'Dec 1, 2023',
    status: 'Expired',
    logoUrl: 'https://picsum.photos/seed/104/40/40'
  }
];

export default function CredentialsPage() {
    return (
        <div className="flex flex-col h-full">
            <header className="flex items-center gap-4 mb-6">
                <h1 className="text-3xl font-bold font-headline">My Credentials</h1>
                <div className="ml-auto flex items-center gap-2">
                    <Button variant="outline" size="icon">
                        <List className="h-4 w-4" />
                    </Button>
                    <Button variant="secondary" size="icon">
                        <LayoutGrid className="h-4 w-4" />
                    </Button>
                </div>
            </header>
            
            <div className="flex items-center gap-4 mb-4">
                <div className="relative flex-1">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input placeholder="Search by name or issuer..." className="pl-8" />
                </div>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="outline" className="gap-1">
                            <ListFilter className="h-3.5 w-3.5" />
                            <span>Filter & Sort</span>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Filter by Type</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuCheckboxItem checked>All</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>Education</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>Employment</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>ID</DropdownMenuCheckboxItem>
                         <DropdownMenuLabel>Filter by Status</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuCheckboxItem>Active</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>Revoked</DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>Expired</DropdownMenuCheckboxItem>
                    </DropdownMenuContent>
                </DropdownMenu>
                 <Button className="gap-1">
                    <PlusCircle className="h-3.5 w-3.5" />
                    <span>Add New</span>
                </Button>
            </div>
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {credentials.map((cred, index) => (
                    <Card key={index}>
                        <CardHeader className="flex flex-row items-start gap-4 space-y-0">
                            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                               {cred.icon}
                            </div>
                            <div className="flex-1">
                                <CardTitle className="text-lg">{cred.schema}</CardTitle>
                                <CardDescription>{cred.issuer}</CardDescription>
                            </div>
                            <Image src={cred.logoUrl} alt={`${cred.issuer} logo`} width={40} height={40} className="rounded-full" data-ai-hint="company logo" />
                        </CardHeader>
                        <CardContent>
                            <div className="flex justify-between text-sm text-muted-foreground">
                                <span>Issued on {cred.date}</span>
                                <span className={`font-semibold ${cred.status === 'Active' ? 'text-accent' : 'text-destructive'}`}>{cred.status}</span>
                            </div>
                        </CardContent>
                        <CardFooter className="gap-2">
                             <Button variant="secondary" className="w-full">
                                View Details
                            </Button>
                            <Button variant="outline" className="w-full">
                                <Share className="mr-2 h-4 w-4" /> Share
                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>

            {/* Empty State
            <div className="flex flex-1 items-center justify-center rounded-lg border border-dashed shadow-sm">
                <div className="flex flex-col items-center gap-1 text-center">
                    <h3 className="text-2xl font-bold tracking-tight">You have no credentials</h3>
                    <p className="text-sm text-muted-foreground">Get your first credential by scanning a QR code.</p>
                    <Button className="mt-4">
                        <PlusCircle className="mr-2 h-4 w-4" />
                        Get Credential
                    </Button>
                </div>
            </div> 
            */}
        </div>
    );
}
