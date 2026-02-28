import os

# 1. Define the updated, comprehensive Flutter code
flutter_code = '''
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

late List<CameraDescription> _cameras;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  _cameras = await availableCameras();
  runApp(const EBayCameraApp());
}

class EBayCameraApp extends StatelessWidget {
  const EBayCameraApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData.dark(),
      home: const EBayListerHome(),
    );
  }
}

class EBayListerHome extends StatefulWidget {
  const EBayListerHome({super.key});
  @override
  State<EBayListerHome> createState() => _EBayListerHomeState();
}

class _EBayListerHomeState extends State<EBayListerHome> {
  CameraController? _controller;
  int _counter = 1001;
  String _category = 'Tops';
  String _condition = '3000'; // Pre-owned
  
  final Map<String, XFile?> _photos = {
    'Front': null, 'Back': null, 'Tag': null, 'Detail': null, 'Defect': null, 'Bonus': null
  };

  // Controllers for all eBay required fields
  final TextEditingController _brandController = TextEditingController();
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _priceController = TextEditingController();
  final TextEditingController _shipController = TextEditingController();
  final TextEditingController _descController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _controller = CameraController(_cameras[0], ResolutionPreset.high);
    _controller!.initialize().then((_) => setState(() {}));
  }

  Future<void> _takePhoto(String angle) async {
    final image = await _controller!.takePicture();
    setState(() => _photos[angle] = image);
  }

  Future<void> _saveItem() async {
    final directory = await getApplicationDocumentsDirectory();
    final String zackPath = p.join(directory.path, 'Zack');
    final String folderName = "${_brandController.text}_${_category}_$_counter".replaceAll(' ', '_');
    final String itemPath = p.join(zackPath, folderName);
    
    await Directory(itemPath).create(recursive: true);

    // 1. Save Photos
    for (var entry in _photos.entries) {
      if (entry.value != null) {
        await File(entry.value!.path).copy(p.join(itemPath, "${entry.key}.jpg"));
      }
    }

    // 2. Generate Full eBay File Exchange CSV
    final File csvFile = File(p.join(zackPath, 'ebay_master_upload.csv'));
    if (!await csvFile.exists()) {
      await csvFile.writeAsString(
        "Action,Category,Title,Description,ConditionID,Format,Duration,StartPrice,Quantity,Location,"
        "ShippingService-1:Option,ShippingService-1:Cost,DispatchTimeMax,CustomLabel\\n"
      );
    }

    String finalTitle = _titleController.text.isEmpty 
        ? "${_brandController.text} $_category ${_notesController.text}" 
        : _titleController.text;
    
    // Formatting the row for CSV (wrapping text in quotes)
    String row = "Add,11483,\\"$finalTitle\\",\\"${_descController.text}\\",$_condition,FixedPrice,GTC,"
        "${_priceController.text},1,\\"Chicago, IL\\",USPSFirstClass,${_shipController.text},3,INV-$_counter\\n";

    await csvFile.writeAsString(row, mode: FileMode.append);

    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Listed & Saved!")));
    _resetForm();
  }

  void _resetForm() {
    setState(() {
      _counter++;
      _photos.updateAll((k, v) => null);
      _brandController.clear();
      _priceController.clear();
      _descController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) return Container();
    return Scaffold(
      appBar: AppBar(title: Text("Inventory #$_counter")),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SizedBox(height: 300, child: CameraPreview(_controller!)),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  TextField(controller: _brandController, decoration: const InputDecoration(labelText: "Brand")),
                  TextField(controller: _priceController, decoration: const InputDecoration(labelText: "Price")),
                  TextField(controller: _shipController, decoration: const InputDecoration(labelText: "Shipping Cost")),
                  TextField(controller: _descController, maxLines: 3, decoration: const InputDecoration(labelText: "Description")),
                  const SizedBox(height: 20),
                  Wrap(
                    spacing: 10,
                    children: _photos.keys.map((angle) => ElevatedButton(
                      onPressed: () => _takePhoto(angle),
                      style: ElevatedButton.styleFrom(backgroundColor: _photos[angle] != null ? Colors.green : null),
                      child: Text(angle),
                    )).toList(),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: _saveItem,
                    style: ElevatedButton.styleFrom(minimumSize: const Size(200, 50), backgroundColor: Colors.blue),
                    child: const Text("SAVE & LIST ITEM"),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
'''

# 2. Write the file
with open('lib/main.dart', 'w') as f:
    f.write(flutter_code)

print("lib/main.dart updated with full eBay File Exchange fields.")