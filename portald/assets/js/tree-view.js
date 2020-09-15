function getData() {
    var data = {
        "id": 1,
        "name": "Ambiente",
        "type": "Root",
        "description": "exacc",
        "children": [
            {
                "id": 2,
                "name": "Host 01",
                "type": "Type",
                "description": "Windows: DESKTOP-VQDVFV4",
                "children": [
                    {
                        "id": 3,
                        "name": "Banco de Dados",
                        "type": "Family",
                        "description": "10.0.0.100",
                        "children": [
                            {
                                "id": 4,
                                "name": "Aplicação",
                                "type": "Organism",
                                "description": "Protheus",
                                "children": [
                                    {
                                        "id": 6,
                                        "name": "Serviço",
                                        "type": "Family",
                                        "description": "Balanceador de Carga",
                                        "children": []
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "name": "Aplicação",
                                "type": "Organism",
                                "description": "TomCat",
                                "children": [
                                    
                                ]
                            }
                        ]
                    },
                ]
            },
            {
                "id": 7,
                "name": "Host 02",
                "type": "Type",
                "description": "Balanceador de Carga",
                "children": [
                    {
                        "id": 8,
                        "name": "Aplicação",
                        "type": "Family",
                        "description": "JBoss Application Server",
                        "children": []
                    },
                ]
            }
        ]
    };

    return data;
}

var data = getData();

var treePlugin = new d3.mitchTree.boxedTree()
                .setAllowFocus(false)
				.setAllowZoom(false)
				.setAllowPan(true)
				.setAllowNodeCentering(false)
				.setData(data)
				.setElement(document.getElementById("visualisation"))
				.setIdAccessor(function(data) {
					return data.id;
				})
				.setChildrenAccessor(function(data) {
					return data.children;
				})
				.setBodyDisplayTextAccessor(function(data) {
					return data.description;
				})
				.setTitleDisplayTextAccessor(function(data) {
					return data.name;
				})
				.initialize();
var nodes = treePlugin.getNodes();
			nodes.forEach(function(node, index, arr) {
				treePlugin.expand(node);
			});
			treePlugin.update(treePlugin.getRoot());