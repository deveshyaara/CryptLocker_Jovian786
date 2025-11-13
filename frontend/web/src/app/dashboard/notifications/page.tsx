import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BellRing, BellOff } from "lucide-react";

const notifications = {
    all: [
        { type: "offer", title: "New Credential Offer from MIT", time: "5m ago" },
        { type: "proof", title: "Proof Request from Tech Corp", time: "1h ago" },
        { type: "connection", title: "Connection Accepted with Verifier", time: "3h ago" },
    ],
    offers: [
        { type: "offer", title: "New Credential Offer from MIT", time: "5m ago" },
    ],
    proofs: [
        { type: "proof", title: "Proof Request from Tech Corp", time: "1h ago" },
    ]
};

export default function NotificationsPage() {
    return (
        <div className="flex flex-col h-full">
            <header className="flex items-center gap-4 mb-6">
                <h1 className="text-3xl font-bold font-headline">Notifications</h1>
                <Button variant="outline" size="sm" className="ml-auto gap-1">
                    <BellRing className="h-4 w-4" />
                    Mark all as read
                </Button>
            </header>
            
            <Tabs defaultValue="all" className="flex-1">
                <TabsList className="grid w-full grid-cols-4">
                    <TabsTrigger value="all">All</TabsTrigger>
                    <TabsTrigger value="offers">Credential Offers</TabsTrigger>
                    <TabsTrigger value="proofs">Proof Requests</TabsTrigger>
                    <TabsTrigger value="connections">Connections</TabsTrigger>
                </TabsList>
                <TabsContent value="all" className="mt-4">
                   {notifications.all.length > 0 ? (
                       <Card>
                           <CardContent className="p-6 text-sm">
                               <div className="space-y-4">
                                   {notifications.all.map((note, i) => (
                                       <div key={i} className="flex items-center">
                                           <p>{note.title}</p>
                                           <p className="ml-auto text-xs text-muted-foreground">{note.time}</p>
                                       </div>
                                   ))}
                               </div>
                           </CardContent>
                       </Card>
                   ) : <EmptyState /> }
                </TabsContent>
                <TabsContent value="offers" className="mt-4">
                    {notifications.offers.length > 0 ? (
                       <Card>
                           <CardContent className="p-6 text-sm">
                               <div className="space-y-4">
                                   {notifications.offers.map((note, i) => (
                                       <div key={i} className="flex items-center">
                                           <p>{note.title}</p>
                                           <p className="ml-auto text-xs text-muted-foreground">{note.time}</p>
                                       </div>
                                   ))}
                               </div>
                           </CardContent>
                       </Card>
                   ) : <EmptyState /> }
                </TabsContent>
                <TabsContent value="proofs" className="mt-4">
                   {notifications.proofs.length > 0 ? (
                       <Card>
                           <CardContent className="p-6 text-sm">
                               <div className="space-y-4">
                                   {notifications.proofs.map((note, i) => (
                                       <div key={i} className="flex items-center">
                                           <p>{note.title}</p>
                                           <p className="ml-auto text-xs text-muted-foreground">{note.time}</p>
                                       </div>
                                   ))}
                               </div>
                           </CardContent>
                       </Card>
                   ) : <EmptyState /> }
                </TabsContent>
                <TabsContent value="connections" className="mt-4">
                   <EmptyState />
                </TabsContent>
            </Tabs>
        </div>
    );
}


function EmptyState() {
    return (
        <div className="flex flex-1 items-center justify-center rounded-lg border border-dashed shadow-sm h-64">
            <div className="flex flex-col items-center gap-2 text-center">
                <BellOff className="h-12 w-12 text-muted-foreground" />
                <h3 className="text-xl font-bold tracking-tight">All caught up</h3>
                <p className="text-sm text-muted-foreground">You have no new notifications.</p>
            </div>
        </div>
    )
}
